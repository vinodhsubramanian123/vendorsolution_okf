from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

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
    allow_origins=["*"],
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

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

import functools

@functools.lru_cache(maxsize=1)
def get_repo() -> RepoManager:
    repo = RepoManager(str(REPOSITORY_PATH), str(PROJECT_ROOT))
    repo.bootstrap()
    return repo

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
        "stats": stats,
        "platforms": platforms
    }

@app.post("/api/query")
async def query_solution(request: QueryRequest):
    repo = get_repo()
    parser = IntentParser()
    try:
        parsed_request = parser.parse_request(request.query)
        generator = SolutionGenerator(repo.graph, repo.vector_store)
        candidates = generator.generate(parsed_request)
        
        # Format candidate rules for UI clarity
        formatted_candidates = []
        for c in candidates:
            c_dict = c.model_dump()
            formatted_evals = []
            if "rule_evaluations" in c_dict:
                for ev in c_dict["rule_evaluations"]:
                    # Try to fetch actual rule text from graph if available
                    rule_text = "Unknown Rule"
                    if "rule_id" in ev and ev["rule_id"] in repo.graph.graph:
                        rule_data = repo.graph.graph.nodes[ev["rule_id"]]
                        rule_text = rule_data.get("description") or rule_data.get("title") or ev["rule_id"]
                    
                    # Instead of generic title, use the text
                    formatted_evals.append({
                        "rule_id": ev.get("rule_id"),
                        "title": rule_text,
                        "status": ev.get("status"),
                        "severity": ev.get("severity"),
                        "message": ev.get("message", ""),
                        "confidence": ev.get("confidence", "UNKNOWN"),
                        "trace": ev.get("trace", "")
                    })
                c_dict["rule_evaluations"] = formatted_evals
            formatted_candidates.append(c_dict)
            
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
        
    return {
        "status": "success",
        "is_valid": is_valid and boq_result.is_valid,
        "fuzzy_matches": [m.model_dump() for m in boq_result.messages if m.severity == "Info"],
        "invalid_skus": [m.model_dump() for m in boq_result.messages if m.severity == "Error"],
        "corrected_components": corrected_components,
        "rule_evaluations": formatted_rules
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
