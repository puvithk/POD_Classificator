"""Qwen Vision-Language model client."""

import json
import base64
import mimetypes
from ..schemas.pod_schema import PODExtractionResult
from typing import Optional
from configs.config import MODEL_PROVIDER, MODEL_API_KEY
from pydantic import ValidationError


class QwenClient:
    """Client for interacting with Qwen VL models."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "Qwen/Qwen3-VL-8B-Instruct:featherless-ai"):
        self.api_key = api_key or MODEL_API_KEY
    def __init__(self, api_key: Optional[str] = None, model_name: str = "Qwen/Qwen3-VL-8B-Instruct:featherless-ai"):
        self.api_key = api_key or MODEL_API_KEY
        self.model_name = model_name

        if MODEL_PROVIDER == "huggingface":
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(api_key=self.api_key)

        elif MODEL_PROVIDER == "transformers":
            from transformers import AutoProcessor, AutoModelForVision2Seq
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            self.client = AutoModelForVision2Seq.from_pretrained(self.model_name)

        else:
            raise ValueError(f"Unknown MODEL_PROVIDER: {MODEL_PROVIDER}")

    @staticmethod
    def _image_to_data_uri(image_path: str) -> str:
        mime, _ = mimetypes.guess_type(image_path)
        mime = mime or "image/jpeg"
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{encoded}"

    def _invoke_huggingface(self, prompt, image_path):
        data_uri = self._image_to_data_uri(image_path)

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_uri}},
                    ],
                }
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        return completion.choices[0].message.content

    def _invoke_local(self, prompt, image_path):
        import torch
        from PIL import Image

        image = Image.open(image_path).convert("RGB")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        inputs = self.processor(text=[text], images=[image], padding=True, return_tensors="pt")
        inputs = {k: v.to(self.client.device) if hasattr(v, "to") else v for k, v in inputs.items()}

        with torch.inference_mode():
            generated_ids = self.client.generate(
                **inputs, max_new_tokens=1024, temperature=0.2, do_sample=True
            )

        input_token_length = inputs["input_ids"].shape[1]
        generated_ids = generated_ids[:, input_token_length:]

        response = self.processor.batch_decode(
            generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        return response[0].strip()

    def invoke(self, prompt, image_path):
        if MODEL_PROVIDER == "huggingface":
            return self._invoke_huggingface(prompt, image_path)
        else:
            return self._invoke_local(prompt, image_path)

    def generate(self, prompt: str, image_path: Optional[str] = None) -> PODExtractionResult:
        """Send prompt and optional image to Qwen model and return a validated PODExtractionResult."""

        schema_json = json.dumps(PODExtractionResult.model_json_schema(), indent=2)

        full_prompt = (
            f"{prompt}\n\n"
            "Return ONLY a single valid JSON object matching this schema. "
            "No explanation, no markdown, no code fences.\n\n"
            f"Schema:\n{schema_json}"
        )

        raw_response = self.invoke(full_prompt, image_path)
        return raw_response 
        

if __name__ == "__main__":
    client = QwenClient()
    with open("prompts/pod_extraction_prompt.txt", "r") as f:
        prompt = f.read()
    result = client.generate(prompt, "test.jpg")
    print(result)