import json
import re
from typing import Dict, Any, Optional, Tuple
import asyncio
import httpx
from datetime import datetime

from src.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    INFERENCE_TIMEOUT,
    FARA_TEMPERATURE,
    FARA_TOP_P,
    FARA_TOP_K,
    FARA_REPEAT_PENALTY,
    FARA_CONTEXT_WINDOW,
    MAX_RETRIES,
)
from src.utils.logger import get_logger

logger = get_logger("reasoning_engine")


class FaraReasoningEngine:
    """Advanced reasoning using Fara-7B via Ollama"""

    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL
        self.timeout = INFERENCE_TIMEOUT
        self.retry_count = 0
        self.max_retries = MAX_RETRIES

    async def _call_ollama(
        self, prompt: str, temperature: float = FARA_TEMPERATURE
    ) -> Tuple[str, bool]:
        """Call Ollama API and get response"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": temperature,
                        "top_p": FARA_TOP_P,
                        "top_k": FARA_TOP_K,
                        "repeat_penalty": FARA_REPEAT_PENALTY,
                    },
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", ""), True
                else:
                    logger.error(f"Ollama API error: {response.status_code}")
                    return "", False

        except asyncio.TimeoutError:
            logger.error(f"Ollama inference timeout after {self.timeout}s")
            return "", False
        except Exception as e:
            logger.error(f"Ollama call failed: {str(e)}")
            return "", False

    async def analyze_page_state(self, page_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current page state and determine next actions"""
        html = page_state.get("html", "")[:2000]  # Truncate for context
        url = page_state.get("url", "")
        title = page_state.get("title", "")

        prompt = f"""You are an advanced browser automation agent analyzing a webpage state.

## Current Page State
URL: {url}
Title: {title}

HTML (truncated):
{html}

## Task
Analyze this page and provide:
1. Current page type (login, form, dashboard, download, etc.)
2. Key elements present
3. Next recommended action if given a task

Respond in JSON format:
{{
  "page_type": "...",
  "key_elements": [...],
  "recommended_action": "...",
  "analysis": "..."
}}"""

        response, success = await self._call_ollama(prompt)

        if not success:
            logger.error("Failed to analyze page state")
            return {"status": "error", "error": "Inference failed"}

        try:
            # Extract JSON from response
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["status"] = "success"
                return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response")

        return {
            "status": "success",
            "raw_response": response,
            "analysis": response,
        }

    async def generate_browser_actions(
        self,
        objective: str,
        page_state: Dict[str, Any],
        previous_actions: list = None,
        error_context: str = None,
    ) -> Dict[str, Any]:
        """Generate next browser actions based on objective and current state"""
        html = page_state.get("html", "")[:3000]
        url = page_state.get("url", "")

        previous_actions_text = ""
        if previous_actions:
            previous_actions_text = f"\n\nPrevious actions taken:\n{json.dumps(previous_actions[-3:], indent=2)}"

        error_context_text = ""
        if error_context:
            error_context_text = f"\n\nLast error/issue:\n{error_context}\n\nPlease provide corrected selectors or alternative actions."

        prompt = f"""You are an expert Selenium/Playwright automation engineer. Your task is to analyze a webpage and generate precise browser automation steps.

## Objective
{objective}

## Current Page
URL: {url}
HTML (key section):
{html}
{previous_actions_text}
{error_context_text}

## Instructions
1. Analyze the HTML to find relevant elements (buttons, inputs, links)
2. Generate JSON actions for browser automation
3. Each action must have: action, selector, and optional value
4. Selectors must be unique and precise (use CSS or XPath)
5. For errors, suggest alternative selectors

Valid actions: click, fill, goto, wait, download, scroll, key, screenshot

Respond ONLY with valid JSON array of actions:
[
  {{"action": "...", "selector": "...", "value": "...", "reason": "..."}}
]"""

        response, success = await self._call_ollama(prompt, temperature=0.5)

        if not success:
            logger.error("Failed to generate browser actions")
            return {
                "status": "error",
                "error": "Inference failed",
                "actions": [],
            }

        try:
            # Extract JSON array from response
            json_match = re.search(r"\[.*\]", response, re.DOTALL)
            if json_match:
                actions = json.loads(json_match.group())
                logger.info(f"Generated {len(actions)} actions")
                return {
                    "status": "success",
                    "actions": actions,
                    "reasoning": response[:200],
                }
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse actions JSON: {response[:100]}")

        return {
            "status": "error",
            "error": "Failed to parse actions",
            "raw_response": response,
            "actions": [],
        }

    async def extract_information(
        self, text: str, extraction_schema: Dict[str, str]
    ) -> Dict[str, Any]:
        """Extract structured information from text using schema"""
        schema_str = json.dumps(extraction_schema, indent=2)

        prompt = f"""Extract information from the following text according to the schema provided.

## Text
{text[:5000]}

## Extraction Schema
{schema_str}

Return ONLY valid JSON matching the schema. For missing fields, use null.
{{
  "fields": {{ ... }},
  "confidence": 0.95,
  "notes": "..."
}}"""

        response, success = await self._call_ollama(prompt, temperature=0.3)

        if not success:
            logger.error("Failed to extract information")
            return {
                "status": "error",
                "error": "Extraction inference failed",
                "fields": {},
            }

        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["status"] = "success"
                return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse extraction response")

        return {
            "status": "error",
            "error": "Failed to parse extraction",
            "fields": {},
        }

    async def classify_document(self, text: str) -> Dict[str, Any]:
        """Classify document type from extracted text"""
        prompt = f"""Classify the document type from the following text:

{text[:2000]}

Possible types: invoice, receipt, form, id_card, bank_statement, contract, other

Respond with JSON:
{{
  "doc_type": "...",
  "confidence": 0.95,
  "key_indicators": ["..."],
  "summary": "..."
}}"""

        response, success = await self._call_ollama(prompt, temperature=0.3)

        if not success:
            return {
                "status": "error",
                "error": "Classification inference failed",
                "doc_type": "unknown",
            }

        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["status"] = "success"
                return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse classification response")

        return {
            "status": "error",
            "error": "Failed to parse classification",
            "doc_type": "unknown",
        }

    async def determine_next_workflow_step(
        self,
        current_state: str,
        completed_actions: list,
        extracted_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Determine next workflow step based on current state and progress"""
        prompt = f"""You are a workflow decision engine. Based on the current automation state, decide the next step.

## Current State
{current_state}

## Completed Actions
{json.dumps(completed_actions[-5:], indent=2)}

## Extracted Data
{json.dumps(extracted_data, indent=2)}

## Available Next Steps
1. upload - Upload extracted data to destination
2. archive - Archive the processed document
3. validate - Validate extracted data
4. human_review - Escalate for human review
5. continue - Continue with next document
6. complete - Task complete

Decide the best next step and provide reasoning:
{{
  "next_step": "...",
  "confidence": 0.95,
  "reasoning": "...",
  "required_conditions": ["..."]
}}"""

        response, success = await self._call_ollama(prompt, temperature=0.4)

        if not success:
            logger.error("Failed to determine workflow step")
            return {
                "status": "error",
                "error": "Decision inference failed",
                "next_step": "human_review",
            }

        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["status"] = "success"
                return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse workflow decision")

        return {
            "status": "error",
            "next_step": "human_review",
        }

    async def self_correct_selector(
        self,
        failed_selector: str,
        html: str,
        element_description: str,
    ) -> Dict[str, Any]:
        """Self-correct failed selectors by analyzing HTML"""
        html_snippet = html[:3000]

        prompt = f"""A browser selector failed. Analyze the HTML and provide corrected selectors.

## Failed Selector
{failed_selector}

## Element Description
{element_description}

## HTML Context (truncated)
{html_snippet}

Provide corrected selectors in order of preference:
{{
  "corrected_selectors": ["...", "...", "..."],
  "alternative_approach": "...",
  "explanation": "..."
}}"""

        response, success = await self._call_ollama(prompt, temperature=0.2)

        if not success:
            logger.error("Failed to self-correct selector")
            return {
                "status": "error",
                "error": "Self-correction inference failed",
                "corrected_selectors": [],
            }

        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["status"] = "success"
                return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse self-correction response")

        return {
            "status": "error",
            "corrected_selectors": [],
        }
