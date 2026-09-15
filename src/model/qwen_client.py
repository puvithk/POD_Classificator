"""Qwen Vision-Language model client."""

import os
from typing import Any, Dict, Optional
from openai import OpenAI
# pyrefly: ignore [missing-import]
from configs.config import MODEL_PROVIDER , MODEL_API_KEY
from PIL import Image
import torch
import base64
class QwenClient:
    """Client for interacting with Qwen VL models."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "Qwen/Qwen3-VL-8B-Instruct:featherless-ai"):
        self.api_key = api_key or MODEL_API_KEY
        self.model_name = model_name
        if MODEL_PROVIDER == "openrouter":
            self.client = OpenAI(
                base_url="https://router.huggingface.co/v1",
                api_key=self.api_key,
            )
        else : #Transformer qwen 8 model 
            from transformers import AutoProcessor, AutoModelForVision2Seq
            self.processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-8B-Instruct")
            self.client =  AutoModelForVision2Seq.from_pretrained("Qwen/Qwen2.5-VL-8B-Instruct")
    
    def _invoke_local(self , prompt , image_path):
        image = Image.open(image_path).convert("RGB")

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ]

        # Convert messages into Qwen's expected chat format
        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        # Process both text and image
        inputs = self.processor(
            text=[text],
            images=[image],
            padding=True,
            return_tensors="pt",
        )

        # Move tensors to the model device
        inputs = {
            key: value.to(self.client.device)
            if hasattr(value, "to")
            else value
            for key, value in inputs.items()
        }

        # Generate response
        with torch.inference_mode():
            generated_ids = self.client.generate(
                **inputs,
                max_new_tokens=1024,
                temperature=0.2,
                do_sample=True,
            )

        # Remove the input tokens from the generated output
        input_token_length = inputs["input_ids"].shape[1]

        generated_ids = generated_ids[:, input_token_length:]

        # Decode model response
        response = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )

        return response[0].strip()



    def _invoke_openroute(self, prompt, image_path):
        with open(image_path, "rb") as f:
            b64_image = base64.b64encode(f.read()).decode("utf-8")

        ext = image_path.rsplit(".", 1)[-1].lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext  # png, webp, etc.

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{mime};base64,{b64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1024,
            temperature=0,
        )
        return response.choices[0].message.content
    def invoke(self , prompt , image_path ):
        if MODEL_PROVIDER ==  "openrouter":
           return self._invoke_openroute(prompt , image_path)
        else :
            # If its transformer
            return self._invoke_local(prompt , image_path)


    def generate(self, prompt: str, image_path: Optional[str] = None) -> Dict[str, Any]:
        """Send prompt and optional image to Qwen model and return response."""
        raise NotImplementedError("Implement Qwen API call here.")




# -----------------------------------------

if __name__ == "__main__":
    qwen_client = QwenClient()
    result = qwen_client.invoke("Hello","test.jpeg")
    print(result)
