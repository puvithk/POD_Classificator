"""Extraction pipeline for POD documents."""

from typing import Any, Dict
import json
from ..model.qwen_client import QwenClient
from pydantic import ValidationError
from ..schemas.pod_schema import PODExtractionResult
class PODExtraction:
    def __init__(self):
        pass
        

    def extract_pod_info(self, image_path: str, prompt_path: str) -> PODExtractionResult:
        """Extract structured data from a POD document image."""
        with open(prompt_path, "r") as f:
            prompt = f.read()
        try:
            raw_response = QwenClient().generate(prompt, image_path)
        except Exception as e:
            raise ValueError(f"Model generation failed: {e}") from e

        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Model did not return valid JSON:\n{raw_response}") from e

        try:
            return PODExtractionResult.model_validate(data)
        except ValidationError as e:
            raise ValueError(f"Model output did not match PODExtractionResult schema: {e}") from e


if __name__ == "__main__":
    extractor = PODExtraction()
    result = extractor.extract_pod_info("test.jpg", "prompts/pod_extraction_prompt.txt")
    print(result)