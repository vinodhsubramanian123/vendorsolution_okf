"""
LLM Client — Centralized Gemini Integration

Governs: Dynamic Intent Parsing and Intelligent Component Selection (Phase 6).
"""

import os
import json
import logging
import time
import functools
from typing import Any, Dict, List, Tuple
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from langfuse.decorators import observe, langfuse_context

logger = logging.getLogger("ikp.reasoning.llm")


class KeyManager:
    """Manages a pool of Gemini API keys for rotation and failover."""
    
    def __init__(self):
        load_dotenv()
        keys_str = os.environ.get("GEMINI_API_KEYS", os.environ.get("GEMINI_API_KEY", ""))
        self.keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        self.current_idx = 0
        if not self.keys:
            logger.warning("No GEMINI_API_KEYS found in environment. LLM reasoning will fail.")
            
    def get_client(self) -> genai.Client | None:
        if not self.keys:
            return None
        key = self.keys[self.current_idx]
        return genai.Client(api_key=key)
        
    def rotate(self):
        if not self.keys:
            return
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        logger.info(f"Rotated to Gemini API key index {self.current_idx}")


def retry_with_key_rotation(max_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(self, *args, **kwargs)
                except APIError as e:
                    last_error = e
                    if e.code == 429:
                        logger.warning(f"Rate limit exceeded (HTTP 429) on attempt {attempt+1}. Rotating key...")
                        self.key_manager.rotate()
                        time.sleep(1) # Small backoff before retry
                        continue
                    raise e
                except Exception as e:
                    logger.error(f"LLM API error on attempt {attempt+1}: {e}")
                    raise e
            raise last_error
        return wrapper
    return decorator


# Pydantic Schemas for Structured Output
class Requirement(BaseModel):
    category: str
    name: str
    value: str | int | float
    priority: str

class IntentParseResult(BaseModel):
    workloads: List[str]
    vendor_preference: str | None
    target_platform: str | None
    budget: float | None
    requirements: List[Requirement]

class ComponentSelectionResult(BaseModel):
    selected_component_ids: List[str]
    satisfied_requirements: List[str]
    reasoning_steps: List[str]


class LLMClient:
    """Wrapper for the Gemini LLM API."""

    def __init__(self):
        self.key_manager = KeyManager()

    @observe(as_type="generation", name="parse-intent")
    @retry_with_key_rotation(max_retries=3)
    def parse_intent(self, raw_text: str) -> Dict[str, Any]:
        """
        Ask Gemini to parse natural language intent into structured JSON.
        """
        langfuse_context.update_current_observation(
            input=raw_text,
            model="gemini-2.0-flash",
        )
        prompt = f"You are an expert IT systems engineer parsing a customer request. Extract the requirements from the following request.\n\nRequest: {raw_text}"
        try:
            client = self.key_manager.get_client()
            if not client:
                raise ValueError("No Gemini API client configured")

            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=IntentParseResult,
                )
            )
            # Try to parse the JSON output
            text = response.text.strip()
            return json.loads(text)
        except Exception as e:
            logger.error(f"LLM parse_intent failed: {e}")
            # Fallback to empty if LLM fails
            return {
                "workloads": [],
                "vendor_preference": None,
                "target_platform": None,
                "budget": None,
                "requirements": [],
            }

    @observe(as_type="generation", name="select-components")
    @retry_with_key_rotation(max_retries=3)
    def select_components(
        self,
        platform_id: str,
        available_nodes: Dict[str, Any],
        requirements: List[Dict[str, Any]],
        profile: str = "Balanced",
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Ask Gemini to select the optimal subset of components from a given list that satisfies the requirements.
        Returns: (selected_component_ids, reasoning_steps, satisfied_requirements)
        """
        langfuse_context.update_current_observation(
            input={
                "platform_id": platform_id,
                "requirements": requirements,
                "profile": profile,
                # omitting available_nodes to prevent massive payload traces
            },
            model="gemini-2.0-flash",
        )
        prompt = f"""
You are an expert systems engineer. You are given a platform and a list of available components.
Select the optimal set of component IDs that satisfies the provided customer requirements to form a complete, holistic solution.

CRITICAL HOLISTIC RANKING RULES:
1. You MUST include components that satisfy requirements with priority "required".
2. You MUST include components that satisfy requirements with priority "preferred" if a suitable component is available in the list.
3. Minimize the total number of components selected while meeting these goals.
4. Do NOT downgrade specifications. When substituting parts for the full solution, select alternatives that are strictly equal to or slightly higher in performance/capacity than the requested or failed component.
5. Avoid massive unnecessary upgrades unless no closer alternative exists.
6. Optimize component selection for the following holistic profile: "{profile}".
   - If "Lowest Cost", select the most cost-effective components that STILL MEET OR EXCEED the baseline requirements (no downgrading).
   - If "Performance Optimized", heavily prefer components that are faster, high-end, or enterprise-grade.
   - If "Balanced", balance cost and performance reasonably without dipping below the requested baseline.

Customer Requirements:
{json.dumps(requirements, indent=2)}

Platform: {platform_id}

Available Components:
{json.dumps(available_nodes, indent=2)}
"""
        try:
            client = self.key_manager.get_client()
            if not client:
                raise ValueError("No Gemini API client configured")

            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ComponentSelectionResult,
                )
            )
            text = response.text.strip()
            result = json.loads(text)

            return result.get("selected_component_ids", []), result.get("reasoning_steps", []), result.get("satisfied_requirements", [])
        except Exception as e:
            logger.error(f"LLM select_components failed: {e}")
            return [], [f"LLM failure: {e}"], []

    @observe(as_type="generation", name="generate-embeddings")
    @retry_with_key_rotation(max_retries=5)
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of strings."""
        langfuse_context.update_current_observation(
            input=texts,
            model="gemini-embedding-2"
        )
        try:
            client = self.key_manager.get_client()
            if not client:
                raise ValueError("No Gemini API client configured")

            response = client.models.embed_content(
                model="gemini-embedding-2", contents=texts
            )
            return [e.values for e in response.embeddings]
        except Exception as e:
            logger.error(f"LLM generate_embeddings failed: {e}")
            return [[0.0] * 768 for _ in texts]

    @observe(as_type="generation", name="extract-rules")
    @retry_with_key_rotation(max_retries=3)
    def extract_rules(self, text_chunk: str) -> List[Dict[str, Any]]:
        """Ask Gemini to extract explicit engineering rules from a text chunk."""
        langfuse_context.update_current_observation(
            input=text_chunk,
            model="gemini-2.0-flash"
        )
        prompt = f"""
You are an expert systems engineer. Extract any explicit engineering rules, constraints, or dependencies from the text.
CRITICAL: Preserve literal whitespace and newlines (\n) for long descriptions in rule_text. Do not collapse multi-line bullet points or paragraphs into a single dense line.
Output ONLY valid JSON in the following format:
{{
  "rules": [
    {{
      "rule_text": "description of the rule",
      "severity": "Info|Warning|Error",
      "confidence": "High|Medium|Low|Unverified",
      "targets": ["target1", "target2"]
    }}
  ]
}}

Text:
{text_chunk[:8000]}
"""
        try:
            client = self.key_manager.get_client()
            if not client:
                raise ValueError("No Gemini API client configured")
                
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            text = response.text.strip()
            try:
                parsed = json.loads(text)
                return parsed.get("rules", [])
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from LLM output: {e}\nOutput was: {text[:200]}")
                return []
        except Exception as e:
            logger.error(f"LLM extract_rules failed: {e}")
            return []

    @observe(as_type="generation", name="critic-review-rules")
    @retry_with_key_rotation(max_retries=3)
    def critic_review_rules(self, text_chunk: str) -> List[Dict[str, Any]]:
        """Ask Gemini to find edge-case constraints or subtle dependencies in the text chunk."""
        langfuse_context.update_current_observation(
            input=text_chunk,
            model="gemini-2.0-flash"
        )
        prompt = f"""
You are an expert systems engineering critic. Your job is to find subtle, easily missed edge-case constraints, mutual exclusions, or hidden dependencies in the text. Ignore obvious rules.
CRITICAL: Preserve literal whitespace and newlines (\n) for long descriptions in rule_text. Do not collapse multi-line bullet points or paragraphs into a single dense line.
Output ONLY valid JSON in the following format:
{{
  "rules": [
    {{
      "rule_text": "description of the subtle rule or constraint",
      "severity": "Info|Warning|Error",
      "confidence": "High|Medium|Low|Unverified",
      "targets": ["target1", "target2"]
    }}
  ]
}}

Text:
{text_chunk[:8000]}
"""
        try:
            client = self.key_manager.get_client()
            if not client:
                raise ValueError("No Gemini API client configured")
                
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            text = response.text.strip()
            try:
                parsed = json.loads(text)
                return parsed.get("rules", [])
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from LLM output: {e}\nOutput was: {text[:200]}")
                return []
        except Exception as e:
            logger.error(f"LLM critic_review_rules failed: {e}")
            return []
