from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import os

from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.validation.validator import ManualReviewValidator
from ikp_platform.core.validation.boq_validator import BOQValidator
from ikp_platform.core.ontology.models import EngineeringObjectType

app = FastAPI(title="IKP Reasoning API", version="2.0.0")

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

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

import threading

_repo_lock = threading.Lock()
_repo_instance = None

def get_repo() -> RepoManager:
    global _repo_instance
    if _repo_instance is not None:
        return _repo_instance
        
    with _repo_lock:
        if _repo_instance is not None:
            return _repo_instance
            
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
        _repo_instance = repo
        return _repo_instance

@app.get("/api/status")
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
                "rules": 0
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
        "platforms": platforms
    }

@app.post("/api/query")
async def query_solution(request: QueryRequest):
    repo = get_repo()
    parser = IntentParser()
    try:
        parsed_request = parser.parse_request(request.query)
        generator = SolutionGenerator(repo.graph, repo.vector_store, repo.mcp_client)
        candidates = generator.generate(parsed_request)
        
        # Format candidate output for UI
        formatted_candidates = [c.model_dump() for c in candidates]
            
        return {
            "request_id": parsed_request.request_id,
            "parsed_intent": parsed_request.model_dump(),
            "candidates": formatted_candidates
        }
    except Exception as e:
        logger.error(f"API Error during query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate")
async def validate_solution(request: ValidationRequest):
    repo = get_repo()
    validator = ManualReviewValidator()
    result = validator.validate(request.components, {"solution_id": request.solution_id})
    delta = validator.to_knowledge_delta(result)
    repo._record_delta(delta)
    return {
        "status": "validation_queued",
        "delta_id": delta.delta_id,
        "is_valid": result.is_valid,
        "messages": [m.model_dump() for m in result.messages]
    }

@app.post("/api/boq/validate")
async def validate_boq(request: BOQValidationRequest):
    repo = get_repo()
    
    # 1. Fuzzy match and correct SKUs
    boq_validator = BOQValidator(repo.graph)
    boq_result = boq_validator.validate(request.components, {})
    
    # Record any fuzzy match corrections as a KnowledgeDelta to "learn" typos
    corrections = [m for m in boq_result.messages if m.severity == "Info"]
    if corrections:
        from ikp_platform.core.ontology.models import KnowledgeDelta, DeltaChange, DeltaChangeType, EvidenceRecord, ConfidenceLevel
        import uuid
        
        changes = []
        for msg in corrections:
            # message format from boq_validator: "Auto-corrected requested SKU 'foo' to 'bar'"
            changes.append(
                DeltaChange(
                    change_type=DeltaChangeType.UPDATE_COMPONENT,
                    object_id=msg.affected_object or "unknown",
                    field_name="alias",
                    new_value=msg.message,
                    evidence=EvidenceRecord(
                        source_id="boq_validator",
                        confidence=ConfidenceLevel.MEDIUM,
                        description=msg.message
                    )
                )
            )
        delta = KnowledgeDelta(
            delta_id=f"DELTA-{str(uuid.uuid4())[:8]}",
            source_id="api_boq_validate", 
            changes=changes
        )
        repo._record_delta(delta)
    
    # Extract the corrected component IDs
    corrected_components = []
    for comp in request.components:
        matched_id, _ = boq_validator.fuzzy_match_sku(comp)
        corrected_components.append(matched_id)
        
    # 2. Run rule engine
    engine = RuleEngine(repo.graph)
    
    # Try to find platform in components, otherwise default to first available
    platform_id = "unknown-platform"
    for comp in corrected_components:
        if comp in repo.graph.graph and repo.graph.graph.nodes[comp].get("type") == EngineeringObjectType.PLATFORM.value:
            platform_id = comp
            break
            
    if platform_id == "unknown-platform":
        platforms = [n for n, d in repo.graph.graph.nodes(data=True) if d.get("type") == EngineeringObjectType.PLATFORM.value]
        if platforms:
            platform_id = platforms[0]

    engine_valid, reasoning_chain, errors = engine.evaluate_solution(platform_id, corrected_components)
    
    # 3. Format results for UI
    formatted_rules = []
    
    # Add reasoning chain items as Info
    for step in reasoning_chain:
        formatted_rules.append({
            "title": step,
            "status": "PASS",
            "severity": "Info",
            "message": ""
        })
        
    # Add errors as failures
    for err in errors:
        formatted_rules.append({
            "title": err,
            "status": "FAIL",
            "severity": "Error",
            "message": ""
        })
        
    is_valid = engine_valid and boq_result.is_valid
    
    alternatives = []
    if request.num_options > 0:
        import uuid
        import random
        from ikp_platform.core.ontology.models import CustomerRequest, Requirement
        
        # Build generator to find closest working solutions
        generator = SolutionGenerator(repo.graph, repo.vector_store, repo.mcp_client)
        cust_req = CustomerRequest(
            request_id=f"req-{str(uuid.uuid4())[:8]}",
            target_platform=platform_id,
            workloads=request.workloads,
            requirements=[Requirement(name="Base", value="Match BOQ capabilities")]
        )
        
        candidates = generator.generate(cust_req)
        
        # Mock partner portal pricing/cost metrics for ranking
        for c in candidates:
            c_cost = random.randint(5000, 25000)
            if c.profile == "Lowest Cost":
                c_cost = random.randint(3000, 8000)
            elif c.profile == "Performance Optimized":
                c_cost = random.randint(15000, 30000)
                
            alt_dict = c.model_dump()
            alt_dict["estimated_cost"] = c_cost
            alternatives.append(alt_dict)
            
        # Rank by cost and slice to requested configurable number of options
        alternatives = sorted(alternatives, key=lambda x: x["estimated_cost"])[:request.num_options]
        
    return {
        "status": "success",
        "is_valid": is_valid,
        "fuzzy_matches": [m.model_dump() for m in boq_result.messages if m.severity == "Info"],
        "invalid_skus": [m.model_dump() for m in boq_result.messages if m.severity == "Error"],
        "corrected_components": corrected_components,
        "rule_evaluations": formatted_rules,
        "alternatives": alternatives
    }

@app.post("/api/search")
async def semantic_search(request: SearchRequest):
    repo = get_repo()
    
    # Search vector store
    results = repo.vector_store.semantic_search(request.query, n_results=request.limit)
    
    formatted_results = []
    for res_id in results:
        node_data = {}
        if res_id in repo.graph.graph:
            node_data = repo.graph.graph.nodes[res_id]
            
        formatted_results.append({
            "id": res_id,
            "score": 1.0,
            "text": node_data.get("description", "No description available"),
            "title": node_data.get("title", res_id),
            "type": node_data.get("type", "unknown")
        })
        
    return {
        "query": request.query,
        "results": formatted_results
    }

class ApprovalRequest(BaseModel):
    object_id: str

@app.get("/api/review-queue")
async def get_review_queue():
    repo = get_repo()
    unverified = []
    
    for node_id, data in repo.graph.graph.nodes(data=True):
        conf = data.get("confidence")
        if conf in ["Unverified", "Medium", "Low"]:
            unverified.append({
                "id": node_id,
                "title": data.get("title", node_id),
                "type": data.get("type", "Unknown"),
                "confidence": conf,
                "description": data.get("description", ""),
                "evidence": data.get("evidence", [])
            })
            
    return {"queue": unverified}

@app.post("/api/review-queue/approve")
async def approve_object(request: ApprovalRequest):
    repo = get_repo()
    
    try:
        # We need to load the full object from disk, update it, and save it back
        # to ensure it's properly formatted and serialized in OKF.
        obj_path = None
        # Naive lookup for file path (assuming standard OKF structure)
        # However, okf_reader handles this.
        # But we don't have a direct `get_object` by ID in the reader.
        # So we scan. In a production app, we'd cache file paths.
        all_objs = repo.reader.load_all()
        target_obj = None
        for o in all_objs:
            if o.id == request.object_id:
                target_obj = o
                break
                
        if not target_obj:
            raise HTTPException(status_code=404, detail="Object not found")
            
        from ikp_platform.core.ontology.models import ConfidenceLevel
        target_obj.confidence = ConfidenceLevel.HIGH
        repo.add_concept(target_obj)
        
        return {"status": "success", "message": f"Approved {request.object_id}"}
    except Exception as e:
        logger.error(f"Failed to approve object: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ikp_platform.api:app", host="0.0.0.0", port=8000, reload=True)
