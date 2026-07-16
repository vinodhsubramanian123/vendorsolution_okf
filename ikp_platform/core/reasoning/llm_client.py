"""
LLM Client — Centralized Gemini Integration

Governs: Dynamic Intent Parsing and Intelligent Component Selection (Phase 6).
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional
from google import genai
from dotenv import load_dotenv

logger = logging.getLogger("ikp.reasoning.llm")


class LLMClient:
    """Wrapper for the Gemini LLM API."""

    def __init__(self):
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment. LLM reasoning will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)

    def parse_intent(self, raw_text: str) -> Dict[str, Any]:
        """
        Ask Gemini to parse natural language intent into structured JSON.
        """
        prompt = f"""
You are an expert IT systems engineer parsing a customer request.
Extract the requirements from the following request into a structured JSON format.

JSON Schema Requirements:
{{
  "workloads": ["list of strings (e.g., 'ai', 'virtualization', 'database')"],
  "vendor_preference": "string or null (e.g., 'HPE', 'Dell')",
  "target_platform": "string or null (e.g., 'dl380-gen12', 'hpe-alletra-storage')",
  "budget": number or null,
  "requirements": [
    {{
      "category": "technical|business|operational|commercial",
      "name": "string (e.g., 'Storage Protocol', 'Memory Capacity', 'Accelerator')",
      "value": "string or number",
      "priority": "required|preferred|nice_to_have"
    }}
  ]
}}

Request: {raw_text}

Output ONLY valid JSON.
"""
        try:
            logger.debug(f"LLM parse_intent prompt: {prompt}")
            if not self.client:
                raise ValueError("No Gemini API client configured")
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            # Try to parse the JSON output
            text = response.text.strip()
            logger.info(f"LLM parse_intent response: {text}")

            if text.startswith("```json"):
                text = text.replace("```json", "", 1).rstrip("```").strip()
            
            return json.loads(text)
        except Exception as e:
            logger.error(f"LLM parse_intent failed: {e}")
            # Fallback to empty if LLM fails
            return {"workloads": [], "vendor_preference": None, "target_platform": None, "budget": None, "requirements": []}

    def select_components(self, platform_id: str, available_nodes: Dict[str, Any], requirements: List[Dict[str, Any]]) -> List[str]:
        """
        Ask Gemini to select the optimal subset of components from a given list that satisfies the requirements.
        """
        prompt = f"""
You are an expert systems engineer. You are given a platform and a list of available components.
Select the optimal set of component IDs that satisfies the provided customer requirements.

Rules:
1. You MUST include components that satisfy requirements with priority "required".
2. You MUST include components that satisfy requirements with priority "preferred" if a suitable component is available in the list.
3. Minimize the total number of components selected while meeting these goals.

Customer Requirements:
{json.dumps(requirements, indent=2)}

Platform: {platform_id}

Available Components:
{json.dumps(available_nodes, indent=2)}

Output ONLY valid JSON in the following format:
{{
  "selected_component_ids": ["id1", "id2"],
  "reasoning_steps": ["step 1", "step 2"]
}}
"""
        try:
            logger.debug(f"LLM select_components prompt: {prompt}")
            if not self.client:
                raise ValueError("No Gemini API client configured")
                
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            text = response.text.strip()
            logger.info(f"LLM select_components response: {text}")
            
            if text.startswith("```json"):
                text = text.replace("```json", "", 1).rstrip("```").strip()
                
            result = json.loads(text)
            
            return result.get("selected_component_ids", []), result.get("reasoning_steps", [])
        except Exception as e:
            logger.error(f"LLM select_components failed: {e}")
            return [], [f"LLM failure: {e}"]

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of strings."""
        try:
            if not self.client:
                raise ValueError("No Gemini API client configured")
                
            response = self.client.models.embed_content(
                model='text-embedding-004',
                contents=texts
            )
            # The response from google.genai has an 'embeddings' attribute which is a list of objects 
            # where each object has a 'values' list.
            return [e.values for e in response.embeddings]
        except Exception as e:
            logger.error(f"LLM generate_embeddings failed: {e}")
            return [[0.0] * 768 for _ in texts]

    def extract_rules(self, text_chunk: str) -> List[Dict[str, Any]]:
        """
        Ask Gemini via local Antigravity CLI to extract explicit engineering rules from a text chunk.
        
        NOTE: We intentionally use the `antigravity-cli` here instead of the `google-genai`
        SDK to leverage specialized local extraction prompts and parallel processing configurations
        that the CLI provides for rule mining.
        """
        prompt = f"""
You are an expert systems engineer. Extract any explicit engineering rules, constraints, or dependencies from the text.
Output ONLY valid JSON in the following format:
{{
  "rules": [
    {{
      "rule_text": "description of the rule",
      "severity": "Info|Warning|Error",
      "targets": ["target1", "target2"]
    }}
  ]
}}

Text:
{text_chunk[:8000]}
"""
        import subprocess
        try:
            logger.info("Calling antigravity-cli for rule extraction...")
            result = subprocess.run(
                ["antigravity-cli", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"antigravity-cli failed: {result.stderr}")
                return []
                
            text = result.stdout.strip()
            
            # Clean up potential markdown formatting from CLI output
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif text.startswith("```"):
                text = text.replace("```", "", 1).rstrip("```").strip()
            
            # Sometimes CLI prepends chatter
            json_start = text.find("{")
            json_end = text.rfind("}")
            if json_start != -1 and json_end != -1:
                text = text[json_start:json_end+1]
                
            try:
                parsed = json.loads(text)
                return parsed.get("rules", [])
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from antigravity-cli output: {e}\nOutput was: {text[:200]}")
                return []
        except subprocess.TimeoutExpired:
            logger.error("LLM extract_rules timed out calling antigravity-cli")
            return []
        except Exception as e:
            logger.error(f"LLM extract_rules failed: {e}")
            return []

    def critic_review_rules(self, text_chunk: str) -> List[Dict[str, Any]]:
        """
        Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dependencies in the text chunk.
        
        NOTE: Similar to extract_rules, we intentionally shell out to `antigravity-cli` 
        to leverage specialized critic prompts and local execution options.
        """
        prompt = f"""
You are an expert systems engineering critic. Your job is to find subtle, easily missed edge-case constraints, mutual exclusions, or hidden dependencies in the text. Ignore obvious rules.
Output ONLY valid JSON in the following format:
{{
  "rules": [
    {{
      "rule_text": "description of the subtle rule or constraint",
      "severity": "Info|Warning|Error",
      "targets": ["target1", "target2"]
    }}
  ]
}}

Text:
{text_chunk[:8000]}
"""
        import subprocess
        try:
            logger.info("Calling antigravity-cli for critic review...")
            result = subprocess.run(
                ["antigravity-cli", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"antigravity-cli failed: {result.stderr}")
                return []
                
            text = result.stdout.strip()
            
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif text.startswith("```"):
                text = text.replace("```", "", 1).rstrip("```").strip()
                
            json_start = text.find("{")
            json_end = text.rfind("}")
            if json_start != -1 and json_end != -1:
                text = text[json_start:json_end+1]
            
            try:
                parsed = json.loads(text)
                return parsed.get("rules", [])
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from antigravity-cli output: {e}\nOutput was: {text[:200]}")
                return []
        except subprocess.TimeoutExpired:
            logger.error("LLM critic_review_rules timed out calling antigravity-cli")
            return []
        except Exception as e:
            logger.error(f"LLM critic_review_rules failed: {e}")
            return []

