from abc import ABC, abstractmethod
import os
import json
from mealie.core import root_logger
from mealie.services.openai.types import OpenAIDataInjection, OpenAIImageBase

logger = root_logger.get_logger()

# Try to import google-generativeai
try:
    import google.generativeai as genai
    HAS_GOOGLE_AI = True
except ImportError:
    HAS_GOOGLE_AI = False


class AIProvider(ABC):
    @abstractmethod
    async def get_response(self, prompt: str, message: str, images: list[OpenAIImageBase] | None = None, force_json_response: bool = True) -> str | None:
        pass

    @abstractmethod
    async def generate_image(self, prompt: str) -> bytes | None:
        pass


class OpenAIProvider(AIProvider):
    def __init__(self, service_instance):
        self.service = service_instance

    async def get_response(self, prompt: str, message: str, images: list[OpenAIImageBase] | None = None, force_json_response: bool = True) -> str | None:
        return await self.service._get_raw_response_openai(prompt, message, images, force_json_response)

    async def generate_image(self, prompt: str) -> bytes | None:
        return await self.service._generate_image_openai(prompt)


class GoogleAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model_name = model

    async def get_response(self, prompt: str, message: str, images: list[OpenAIImageBase] | None = None, force_json_response: bool = True) -> str | None:
        if not HAS_GOOGLE_AI:
            logger.error("google-generativeai library not installed.")
            return None

        try:
            genai.configure(api_key=self.api_key)
            # Todo: Verify if model needs specific configuration or if 'gemini-pro' works out of box
            model = genai.GenerativeModel(self.model_name)

            # Construct prompt. simple concatenation for now as Gemini doesn't have strict "system" role in same way
            # or we can use the chat history.
            # But the service passes 'prompt' (system) and 'message' (user).
            
            full_prompt = f"{prompt}\n\n{message}"
            
            # Handling images for input (multimodal) if needed
            # For now, let's assume text-only input or straightforward text generation
            # If force_json_response is True, we might need to instruct the model to output JSON
            
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,
            )
            
            if force_json_response:
                full_prompt += "\n\nPlease provide the response in valid JSON format."
                # Note: Gemini 1.5 Pro supports response_mime_type='application/json' but let's stick to prompt engineering for compat
                
            response = await model.generate_content_async(full_prompt, generation_config=generation_config)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Google AI Request Failed: {e}")
            return None

    async def generate_image(self, prompt: str) -> bytes | None:
        # Google Generative AI Python SDK currently focuses on Gemini (text/multimodal generation).
        # Image generation (Imagen) might not be fully exposed or requires Vertex AI.
        # For now, we return None or log warning.
        logger.warning("Google Image Generation is not fully supported in this provider yet.")
        return None
