from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.repository.repo_watcher import RepositoryWatcher
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.reasoning.remediation_engine import RemediationEngine
from ikp_platform.core.validation.validator import ManualReviewValidator
from ikp_platform.core.validation.boq_validator import BOQValidator
from ikp_platform.core.validation.pipeline import ValidationPipeline, ValidationContext
from ikp_platform.core.ontology.models import EngineeringObjectType
from ikp_platform.core.observability import telemetry_trace
from ikp_platform.core.learning.learning_engine import LearningEngine
from langfuse.decorators import observe, langfuse_context

_repo_instance: Optional[RepoManager] = None
_watcher_instance: Optional[RepositoryWatcher] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _repo_instance
    repo = RepoManager(str(REPOSITORY_PATH), str(PROJECT_ROOT))
    loaded = repo.bootstrap()
    if loaded == 0:
        logger.critical(
            "Repository at %s is EMPTY (0 objects loaded). The API will run "
            "but every query/status/search call will return no results. "
            "This is expected on a fresh clone -- run "
            "`./scripts/bootstrap.sh` (or "
            "`uv run python -m ikp_platform.scripts.ingest_catalog`) to "
            "seed the repository before using the API.",
            REPOSITORY_PATH,
        )
    else:
        # Always sync vector store with graph on startup.
        # We run it in a background thread so the API becomes available
        # immediately; search degrades gracefully while indexing completes.
        import threading
        def _bg_reindex():
            vec_count_before = repo.vector_store.collection.count()
            indexed = repo.reindex_vector_store(batch_size=25)
            logger.info(
                f"[startup] Vector store sync: graph={loaded} objects, "
                f"pre-existing={vec_count_before}, newly-indexed={indexed}, "
                f"total={repo.vector_store.collection.count()}"
            )
        threading.Thread(target=_bg_reindex, daemon=True, name="startup-reindex").start()

    _repo_instance = repo
    
    # Start the repository watcher to track external Obsidian edits
    _watcher_instance = RepositoryWatcher(repo)
    _watcher_instance.start()
    
    yield
    
    if _watcher_instance:
        _watcher_instance.stop()
        
    _repo_instance = None
    langfuse_context.flush()


app = FastAPI(title="IKP Reasoning API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    # `allow_origins=["*"]` combined with `allow_credentials=True` is
    # invalid per the CORS spec (browsers reject it outright), so we
    # take an explicit allowlist instead. Override via CORS_ALLOWED_ORIGINS
    # (comma-separated) for non-local deployments.
    allow_origins=os.environ.get(
        "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).parent.parent
REPOSITORY_PATH = PROJECT_ROOT / "repository"

logger = logging.getLogger("ikp.api")


class QueryRequest(BaseModel):
    query: str


class ValidationRequest(BaseModel):
    solution_id: str
    components: List[str]


class BOQValidationRequest(BaseModel):
    components: List[str]
    num_options: int = 3
    workloads: List[str] = []
    platform_id: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    filter_metadata: Optional[Dict[str, Any]] = None


def get_repo() -> RepoManager:
    if _repo_instance is None:
        raise RuntimeError("Repository not initialized. Is the lifespan active?")
    return _repo_instance


def _infer_platforms_for_components(
    repo: RepoManager, component_ids: List[str]
) -> set[str]:
    """Infer possible platforms from explicit platform IDs and compatibility links."""
    explicit_platforms = set()
    platform_counts: Dict[str, int] = {}

    for comp_id in component_ids:
        if comp_id not in repo.graph.graph:
            continue

        node = repo.graph.graph.nodes[comp_id]
        if node.get("type") == EngineeringObjectType.PLATFORM.value:
            explicit_platforms.add(comp_id)
            continue

        comp_platforms = set()
        for related_id in repo.graph.get_related(comp_id, "Compatible With"):
            if (
                related_id in repo.graph.graph
                and repo.graph.graph.nodes[related_id].get("type")
                == EngineeringObjectType.PLATFORM.value
            ):
                comp_platforms.add(related_id)

        component_id = node.get("component_id")
        if component_id and component_id in repo.graph.graph:
            for related_id in repo.graph.get_related(component_id, "Compatible With"):
                if (
                    related_id in repo.graph.graph
                    and repo.graph.graph.nodes[related_id].get("type")
                    == EngineeringObjectType.PLATFORM.value
                ):
                    comp_platforms.add(related_id)

        for p in comp_platforms:
            platform_counts[p] = platform_counts.get(p, 0) + 1

    if explicit_platforms:
        return explicit_platforms

    if platform_counts:
        max_count = max(platform_counts.values())
        return {p for p, c in platform_counts.items() if c == max_count}

    return set()


@app.get("/api/status")
@telemetry_trace
async def get_status():
    repo = get_repo()
    stats = repo.graph.get_stats()

    # Calculate product-specific KPIs
    platforms = {}
    for node_id, data in repo.graph.graph.nodes(data=True):
        if data.get("type") == EngineeringObjectType.PLATFORM.value:
            platforms[node_id] = {
                "title": data.get("title", node_id),
                "skus": 0,
                "categories": 0,
                "rules": 0,
            }

    for node_id, data in repo.graph.graph.nodes(data=True):
        for plat_id in platforms:
            if node_id.startswith(f"{plat_id}/"):
                obj_type = data.get("type")
                if obj_type == EngineeringObjectType.SKU.value:
                    platforms[plat_id]["skus"] += 1
                elif obj_type == EngineeringObjectType.SOLUTION_CATEGORY.value:
                    platforms[plat_id]["categories"] += 1
                elif obj_type == EngineeringObjectType.RULE.value:
                    platforms[plat_id]["rules"] += 1

    return {
        "status": "online",
        "repository_seeded": stats.get("total_nodes", 0) > 0,
        "stats": stats,
        "platforms": platforms,
    }


@app.post("/api/query")
@observe(name="query-solution")
@telemetry_trace
async def query_solution(request: QueryRequest):
    repo = get_repo()
    try:
        from ikp_platform.core.workflow.executor import WorkflowExecutor
        
        executor = WorkflowExecutor(repo.graph, repo.vector_store, repo.mcp_client)
        result = executor.execute_query(request.query)

        if result.get("requires_human_intervention"):
            return {
                "status": "needs_human_review",
                "message": "Automated recovery exhausted. Solution requires human intervention.",
                "human_review_payload": result.get("human_review_payload"),
                "candidates": [c for c in result.get("ranked_solutions", [])],
                "parsed_intent": result.get("customer_requirements", {}).get("parsed", [])
            }

        return {
            "status": "success",
            "request_id": result.get("customer_requirements", {}).get("request_id", "REQ-UNKNOWN"),
            "parsed_intent": result.get("customer_requirements", {}).get("parsed", []),
            "candidates": [c for c in result.get("ranked_solutions", [])],
            "platform": result.get("platform"),
            "bom": result.get("bom")
        }
    except Exception as e:
        logger.error(f"API Error during query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status/integrations")
@telemetry_trace
async def get_integrations_status():
    repo = get_repo()
    
    # LLM Status
    import os
    has_gemini = bool(os.environ.get("GEMINI_API_KEY"))
    llm_status = "Available" if has_gemini else "Not Configured"
    
    # Vector Index Status
    vector_status = "Available" if hasattr(repo, "vector_store") and repo.vector_store else "Not Configured"
    
    # MCP Status
    has_mcp = bool(os.environ.get("OBSIDIAN_MCP_URL")) or bool(os.environ.get("MCP_SERVER_URL"))
    mcp_status = "Configured" if has_mcp else "Not Configured"
        
    return {
        "integrations": {
            "llm": {"status": llm_status, "name": "Gemini API"},
            "vector_index": {"status": vector_status, "name": "ChromaDB"},
            "mcp": {"status": mcp_status, "name": "Obsidian MCP"}
        }
    }


@app.post("/api/validate")
@telemetry_trace
async def validate_solution(request: ValidationRequest):
    repo = get_repo()
    validator = ManualReviewValidator()
    result = validator.validate(
        request.components, {"solution_id": request.solution_id}
    )
    delta = validator.to_knowledge_delta(result)
    repo._record_delta(delta)
    return {
        "status": "validation_queued",
        "delta_id": delta.delta_id,
        "is_valid": result.is_valid,
        "messages": [m.model_dump() for m in result.messages],
    }


@app.post("/api/boq/validate")
@observe(name="validate-boq")
@telemetry_trace
async def validate_boq(request: BOQValidationRequest, background_tasks: BackgroundTasks):
    repo = get_repo()
    
    # 1. Setup Pipeline and Context
    initial_context = ValidationContext(
        platform_id=request.platform_id,
        original_components=request.components,
    )
    
    pipeline = ValidationPipeline([
        BOQValidator(repo.graph, repo.vector_store),
        RuleEngine(repo.graph),
        RemediationEngine(repo.graph)
    ])
    
    # 2. Infer platform if necessary
    platform_id = request.platform_id
    if not platform_id:
        boq_val = BOQValidator(repo.graph, repo.vector_store)
        corrected = []
        for requested_sku in request.components:
            matched_id, _, _, _ = boq_val.fuzzy_match_sku(requested_sku)
            corrected.append(matched_id)
            
        found_platforms = _infer_platforms_for_components(repo, corrected)

        if len(found_platforms) > 1:
            return {
                "status": "error",
                "is_valid": False,
                "fuzzy_matches": [],
                "invalid_skus": [{"severity": "Error", "message": "Multiple platforms detected in BOQ. Please explicitly specify platform_id."}],
                "corrected_components": corrected,
                "rule_evaluations": [],
                "alternatives": [],
            }
        elif len(found_platforms) == 1:
            initial_context.platform_id = found_platforms.pop()
        else:
            return {
                "status": "error",
                "is_valid": False,
                "fuzzy_matches": [],
                "invalid_skus": [{"severity": "Error", "message": "No platform specified and could not infer platform from components. Please explicitly specify platform_id."}],
                "corrected_components": corrected,
                "rule_evaluations": [],
                "alternatives": [],
            }
            
    # 3. Execute Pipeline
    context = pipeline.execute(initial_context)

    # 4. Record any fuzzy match corrections as a KnowledgeDelta to "learn" typos
    corrections = [m for m in context.messages if m.severity == "Info"]
    if corrections:
        from ikp_platform.core.ontology.models import (
            KnowledgeDelta,
            DeltaChange,
            DeltaChangeType,
            EvidenceRecord,
            ConfidenceLevel,
        )
        import uuid
        changes = []
        for msg in corrections:
            import re
            match = re.search(r"Auto-corrected requested SKU '(.*?)' to", msg.message)
            alias_val = match.group(1) if match else msg.message
            changes.append(
                DeltaChange(
                    change_type=DeltaChangeType.UPDATE_COMPONENT,
                    object_id=msg.affected_object or "unknown",
                    field_name="aliases",
                    new_value=alias_val,
                    evidence=EvidenceRecord(
                        source_id="boq_validator",
                        confidence=ConfidenceLevel.MEDIUM,
                        description=msg.message,
                    ),
                )
            )
        delta = KnowledgeDelta(
            delta_id=f"DELTA-{str(uuid.uuid4())[:8]}",
            source_id="api_boq_validate",
            changes=changes,
        )

        objects_to_update = []
        for change in changes:
            rel_path = repo.reader.path_cache.get(change.object_id)
            if rel_path:
                full_path = repo.repository_path / rel_path
                try:
                    objs = repo.reader._parse_file(full_path)
                    for obj in objs:
                        if obj.id == change.object_id:
                            if change.new_value and str(change.new_value) not in obj.aliases:
                                obj.aliases.append(str(change.new_value))
                            objects_to_update.append(obj)
                except Exception as e:
                    logger.error(f"Failed to load object {change.object_id} for learning: {e}")

        learning_engine = LearningEngine(repo)
        from ikp_platform.core.ontology.models import DeltaStatus
        delta.status = DeltaStatus.VALIDATED
        learning_engine.pending_deltas.append(delta)
        learning_engine.process_validated_deltas(objects_to_update)
        background_tasks.add_task(repo.reindex_vector_store)

    # 5. Format results for UI
    formatted_rules = []

    # Add passed rules from metadata
    passed_rules = context.metadata.get("passed_rules", [])
    for rule in passed_rules:
        formatted_rules.append(
            {
                "title": rule.get("title", ""),
                "status": "PASS",
                "severity": "Info",
                "message": "",
                "category": rule.get("category", "General"),
                "subcategory": rule.get("subcategory", "General")
            }
        )

    # Add errors as failures
    for err in context.errors:
        remedies = getattr(err, "remediations", [])
        payload = getattr(err, "payload", {})
        formatted_rules.append(
            {
                "title": err.message if hasattr(err, "message") else str(err),
                "status": "FAIL",
                "severity": "Error",
                "message": "",
                "remediations": remedies,
                "category": payload.get("category", "General"),
                "subcategory": payload.get("subcategory", "General")
            }
        )

    is_valid = context.is_valid

    alternatives = []
    if request.num_options > 0:
        import uuid
        from ikp_platform.core.ontology.models import (
            CustomerRequest,
            CustomerRequirement,
        )

        # Build generator to find closest working solutions
        generator = SolutionGenerator(repo.graph, repo.vector_store, repo.mcp_client)
        cust_req = CustomerRequest(
            request_id=f"req-{str(uuid.uuid4())[:8]}",
            target_platform=context.platform_id,
            workloads=request.workloads,
            requirements=[
                CustomerRequirement(
                    category="technical", name="Base", value="Match BOQ capabilities"
                )
            ],
        )

        candidates = generator.generate(cust_req)

        # Placeholder cost estimates by profile
        _PROFILE_COST_MAP = {
            "Lowest Cost": 5000,
            "Balanced": 12000,
            "Performance Optimized": 22000,
            "AI Optimized": 28000,
            "Growth Optimized": 15000,
        }
        for c in candidates:
            c_cost = _PROFILE_COST_MAP.get(c.profile, 12000)
            alt_dict = c.model_dump()
            alt_dict["estimated_cost"] = c_cost
            alternatives.append(alt_dict)

        # Rank by cost and slice
        alternatives = sorted(alternatives, key=lambda x: x["estimated_cost"])[
            : request.num_options
        ]

    return {
        "status": "success",
        "is_valid": is_valid,
        "fuzzy_matches": [
            m.model_dump() for m in context.messages if m.severity == "Info"
        ],
        "invalid_skus": [
            m.model_dump() for m in context.messages if m.severity == "Error"
        ],
        "corrected_components": context.corrected_components,
        "rule_evaluations": formatted_rules,
        "alternatives": alternatives,
    }


@app.post("/api/search")
@observe(name="semantic-search")
@telemetry_trace
async def semantic_search(request: SearchRequest):
    repo = get_repo()

    # Gap 7.2: Structured search query logging
    logger.info(
        f"SEMANTIC_SEARCH|query='{request.query}'|limit={request.limit}|filter={request.filter_metadata}"
    )

    # Use Hybrid Search via RepoManager
    formatted_results = repo.search(
        query=request.query, limit=request.limit, filter_metadata=request.filter_metadata
    )

    # Phase 3: Faceted search — compute category/subcategory counts alongside results
    facets: dict = {"category": {}, "subcategory": {}, "vendor": {}, "type": {}}
    for r in formatted_results:
        cat = r.get("category") or "Unknown"
        subcat = r.get("subcategory") or "Unknown"
        vendor = r.get("vendor") or "Unknown"
        obj_type = r.get("type") or "Unknown"
        facets["category"][cat] = facets["category"].get(cat, 0) + 1
        facets["subcategory"][subcat] = facets["subcategory"].get(subcat, 0) + 1
        facets["vendor"][vendor] = facets["vendor"].get(vendor, 0) + 1
        facets["type"][obj_type] = facets["type"].get(obj_type, 0) + 1

    return {"query": request.query, "total": len(formatted_results), "facets": facets, "results": formatted_results}

@app.get("/api/components")
@telemetry_trace
async def get_components(
    platform_id: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    obj_type: str = "Component",
    limit: int = 100,
):
    """Structured query for components — no semantic search required.
    
    Filters:
    - platform_id: e.g. 'hpe-proliant-dl380-gen12'
    - category: e.g. 'Memory', 'Storage', 'CPU', 'GPU'
    - subcategory: e.g. 'DIMM', 'Drive', 'NVMe'
    - obj_type: 'Component', 'SKU', 'Rule', 'Category Limit'
    """
    repo = get_repo()
    results = repo.graph.filter_by_category(
        platform_id=platform_id,
        category=category,
        subcategory=subcategory,
        obj_type=obj_type,
    )
    formatted = []
    for item in results[:limit]:
        formatted.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "description": item.get("description"),
            "category": item.get("component_category") or item.get("attr_component_category"),
            "subcategory": item.get("component_subcategory") or item.get("attr_component_subcategory"),
            "platform_id": item.get("platform_id"),
            "part_number": item.get("part_number") or item.get("attr_part_number"),
            "confidence": item.get("confidence"),
            "lifecycle_status": item.get("lifecycle_status"),
            "vendor": item.get("vendor"),
            "generation": item.get("generation"),
        })
    return {"count": len(formatted), "components": formatted}


@app.get("/api/platforms/{platform_id}/bom")
@telemetry_trace
async def get_platform_bom(platform_id: str):
    """Return full Bill of Materials for a platform, grouped by component category."""
    repo = get_repo()
    if platform_id not in repo.graph.graph:
        all_platforms = repo.graph.filter_by_type("Platform")
        matches = [p for p in all_platforms if platform_id.lower() in p.lower()]
        if not matches:
            return {"error": f"Platform '{platform_id}' not found", "platforms": all_platforms}
        platform_id = matches[0]

    bom = repo.graph.get_platform_bill_of_materials(platform_id)
    platform_data = repo.graph.graph.nodes.get(platform_id, {})
    return {
        "platform_id": platform_id,
        "platform_title": platform_data.get("title", platform_id),
        "category_count": len(bom),
        "total_components": sum(len(v) for v in bom.values()),
        "bom": bom,
    }



class ApprovalRequest(BaseModel):
    object_id: str
    reviewer: str = "Human"
    reason: str = ""


@app.get("/api/review-queue")
@telemetry_trace
async def get_review_queue():
    repo = get_repo()
    unverified = []

    for node_id, data in repo.graph.graph.nodes(data=True):
        conf = data.get("confidence")
        if conf in ["Unverified", "Medium", "Low"]:
            unverified.append(
                {
                    "id": node_id,
                    "title": data.get("title", node_id),
                    "type": data.get("type", "Unknown"),
                    "confidence": conf,
                    "description": data.get("description", ""),
                    "evidence": data.get("evidence", []),
                }
            )

    return {"queue": unverified}


@app.post("/api/review-queue/approve")
@telemetry_trace
async def approve_object(request: ApprovalRequest, background_tasks: BackgroundTasks):
    repo = get_repo()

    try:
        target_obj = None
        
        # Use path_cache instead of full scan
        rel_path = repo.reader.path_cache.get(request.object_id)
        if rel_path:
            full_path = repo.repository_path / rel_path
            objs = repo.reader._parse_file(full_path)
            target_obj = next((o for o in objs if o.id == request.object_id), None)

        if not target_obj:
            raise HTTPException(status_code=404, detail="Object not found")

        from ikp_platform.core.ontology.models import ConfidenceLevel, HistoryEntry, DeltaChangeType
        import datetime

        target_obj.confidence = ConfidenceLevel.HIGH  # type: ignore
        
        # Unify review surfaces: capture rationale
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        msg = f"[{timestamp}] Approved by {request.reviewer}"
        if request.reason:
            msg += f": {request.reason}"
        if not hasattr(target_obj, "history"):
            target_obj.history = []
        target_obj.history.append(
            HistoryEntry(
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                change_type=DeltaChangeType.UPDATED_ATTRIBUTE,
                field_name="confidence",
                new_value="High",
                reason=msg,
            )
        )

        repo.add_concept(target_obj)

        background_tasks.add_task(repo.reindex_vector_store)

        return {"status": "success", "message": f"Approved {request.object_id}"}
    except Exception as e:
        logger.error(f"Failed to approve object: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/review-queue/deltas")
@telemetry_trace
async def get_pending_deltas():
    repo = get_repo()
    if not hasattr(repo, "learning_engine"):
        from ikp_platform.core.learning.learning_engine import LearningEngine
        repo.learning_engine = LearningEngine(repo)  # type: ignore
    deltas = repo.learning_engine.get_pending_reviews()  # type: ignore
    return {"deltas": [d.model_dump(mode="json") for d in deltas]}

@app.post("/api/review-queue/deltas/{delta_id}/approve")
@telemetry_trace
async def approve_delta(delta_id: str, background_tasks: BackgroundTasks, reviewer: str = "Human"):
    repo = get_repo()
    if not hasattr(repo, "learning_engine"):
        from ikp_platform.core.learning.learning_engine import LearningEngine
        repo.learning_engine = LearningEngine(repo)  # type: ignore
        
    success = repo.learning_engine.approve_delta(delta_id, reviewer)  # type: ignore
    if success:
        repo.learning_engine.process_validated_deltas(repo.reader.load_all())  # type: ignore
        background_tasks.add_task(repo.reindex_vector_store)
        return {"status": "success", "message": f"Approved and merged delta {delta_id}"}
    raise HTTPException(status_code=404, detail="Delta not found or not pending")

@app.post("/api/review-queue/deltas/{delta_id}/reject")
@telemetry_trace
async def reject_delta(delta_id: str, reviewer: str = "Human", reason: str = ""):
    repo = get_repo()
    if not hasattr(repo, "learning_engine"):
        from ikp_platform.core.learning.learning_engine import LearningEngine
        repo.learning_engine = LearningEngine(repo)  # type: ignore
        
    success = repo.learning_engine.reject_delta(delta_id, reviewer, reason)  # type: ignore
    if success:
        return {"status": "success", "message": f"Rejected delta {delta_id}"}
    raise HTTPException(status_code=404, detail="Delta not found or not pending")


# ---------------------------------------------------------------------------
# Phase 6f — Human-in-the-Loop Feedback Endpoint
# ---------------------------------------------------------------------------

@app.post("/api/feedback")
@telemetry_trace
async def submit_feedback(payload: dict, background_tasks: BackgroundTasks):
    """
    Phase 6: Human-in-the-loop feedback endpoint.
    Partners / reviewers submit corrections here.
    The feedback is transformed into a KnowledgeDelta and routed to the learning engine.

    Example body:
    {
      "component_id": "hpe-proliant-dl380-gen12/components/memory-ddr5",
      "platform_id": "hpe-proliant-dl380-gen12",
      "correction_type": "AttributeFix",
      "corrected_value": "32GB DDR5 RDIMM 4800 MT/s",
      "field_name": "description",
      "evidence_source": "HPE QuickSpecs DL380 Gen12 Page 42",
      "reviewer_notes": "Wrong description - updated to match vendor spec"
    }
    """
    from ikp_platform.core.learning.feedback_template import HumanFeedback, apply_feedback, CorrectionType

    try:
        # Validate payload
        correction_type_raw = payload.get("correction_type", "AttributeFix")
        try:
            correction_type = CorrectionType(correction_type_raw)
        except ValueError:
            correction_type = CorrectionType.ATTRIBUTE_FIX

        feedback = HumanFeedback(
            component_id=payload.get("component_id"),
            platform_id=payload.get("platform_id"),
            correction_type=correction_type,
            corrected_value=payload.get("corrected_value"),
            field_name=payload.get("field_name"),
            evidence_source=payload.get("evidence_source", "Human reviewer"),
            reviewer_notes=payload.get("reviewer_notes", ""),
        )

        repo = get_repo()
        apply_feedback(feedback, repo)

        # Trigger background reindex so the correction is reflected immediately
        background_tasks.add_task(repo.reindex_vector_store)

        logger.info(f"[Phase 6] Feedback {feedback.feedback_id} submitted: {feedback.correction_type} on {feedback.component_id or feedback.platform_id}")
        return {
            "status": "accepted",
            "feedback_id": feedback.feedback_id,
            "message": "Feedback received and queued as a Knowledge Delta for review",
        }
    except Exception as e:
        logger.error(f"[Phase 6] Feedback submission failed: {e}", exc_info=True)
        raise HTTPException(status_code=422, detail=f"Feedback processing failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ikp_platform.api:app",
        host=os.environ.get("IKP_API_HOST", "127.0.0.1"),
        port=int(os.environ.get("IKP_API_PORT", "8000")),
        reload=os.environ.get("IKP_API_RELOAD", "true").lower()
        in ("1", "true", "yes", "on"),
    )
