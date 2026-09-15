"""JSON extraction and parsing utilities."""

import json
import re
from typing import Any, Dict


def parse_json_from_response(text: str) -> Dict[str, Any]:
    """Extract and parse JSON object from LLM response string."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No valid JSON found in response.")
