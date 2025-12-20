import os
from pathlib import Path
from textwrap import dedent

from openai import NOT_GIVEN, AsyncOpenAI
from openai.types.chat import ChatCompletion
from sqlalchemy.orm import Session

from mealie.core.config import get_app_settings
from mealie.db.db_setup import session_context
from mealie.services.admin.settings_service import SettingsService
from mealie.services.openai.types import OpenAIDataInjection, OpenAIImageBase
from mealie.services.openai.providers import OpenAIProvider, GoogleAIProvider, AIProvider

from .._base_service import BaseService


class OpenAIService(BaseService):
    PROMPTS_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "prompts"

    def __init__(self, session: Session | None = None) -> None:
        super().__init__()
        
        self.ai_provider = "openai"
        self.google_api_key = None
        self.google_model = "gemini-pro"
        
        def load_settings(sess: Session):
            service = SettingsService(sess)
            self.model = service.get_effective_openai_model()
            self.api_key = service.get_effective_openai_api_key()
            
            self.ai_provider = service.get_effective_ai_provider()
            self.google_api_key = service.get_effective_google_api_key()
            self.google_model = service.get_effective_google_model()

            db_settings = service.get_settings()
            self.base_url = db_settings.openai_base_url or self.settings.OPENAI_BASE_URL
            
        if session:
            load_settings(session)
        else:
            with session_context() as sess:
                load_settings(sess)

        self.workers = self.settings.OPENAI_WORKERS
        self.send_db_data = self.settings.OPENAI_SEND_DATABASE_DATA
        self.enable_image_services = self.settings.OPENAI_ENABLE_IMAGE_SERVICES

        self.get_client = lambda: AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=self.settings.OPENAI_REQUEST_TIMEOUT,
            default_headers=self.settings.OPENAI_CUSTOM_HEADERS,
            default_query=self.settings.OPENAI_CUSTOM_PARAMS,
        )

        # Initialize Provider
        self.provider: AIProvider
        if self.ai_provider == "google":
            if self.google_api_key:
                self.provider = GoogleAIProvider(self.google_api_key, self.google_model)
            else:
                 self.logger.warning("Google AI selected but no API key found. Falling back to OpenAI (without key if masked).")
                 self.provider = OpenAIProvider(self)
        else:
            self.provider = OpenAIProvider(self)

        super().__init__()

    @classmethod
    def get_prompt(cls, name: str, data_injections: list[OpenAIDataInjection] | None = None) -> str:
        """
        Load stored prompt and inject data into it.

        Access prompts with dot notation.
        For example, to access `prompts/recipes/parse-recipe-ingredients.txt`, use
        `recipes.parse-recipe-ingredients`
        """

        if not name:
            raise ValueError("Prompt name cannot be empty")

        tree = name.split(".")
        prompt_dir = os.path.join(cls.PROMPTS_DIR, *tree[:-1], tree[-1] + ".txt")
        try:
            with open(prompt_dir) as f:
                content = f.read()
        except OSError as e:
            raise OSError(f"Unable to load prompt {name}") from e

        if not data_injections:
            return content

        content_parts = [content]
        for data_injection in data_injections:
            content_parts.append(
                dedent(
                    f"""
                    ###
                    {data_injection.description}
                    ---

                    {data_injection.value}
                    """
                )
            )
        return "\n".join(content_parts)

    async def _get_raw_response_openai(self, prompt: str, content: list[dict], force_json_response=True) -> str | None:
        # Renamed from _get_raw_response and modified to return str content directly to match provider interface
        # Wait, OpenAIProvider expects raw response or string?
        # My OpenAIProvider implementation: return await self.service._get_raw_response_openai(...)
        # And OpenAIProvider.get_response signature -> str | None
        # So this method should return str | None.
        
        try:
            client = self.get_client()
            response = await client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    },
                    {
                        "role": "user",
                        "content": content,
                    },
                ],
                model=self.model,
                response_format={"type": "json_object"} if force_json_response else NOT_GIVEN,
            )
            if not response.choices:
                return None
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI Request Failed: {e}")
            return None

    async def get_response(
        self,
        prompt: str,
        message: str,
        *,
        images: list[OpenAIImageBase] | None = None,
        force_json_response=True,
    ) -> str | None:
        """Send data to AI Provider and return the response message content"""
        if images and not self.enable_image_services:
            self.logger.warning("AI image services are disabled, ignoring images")
            images = None

        try:
            return await self.provider.get_response(prompt, message, images, force_json_response)
        except Exception as e:
            raise Exception(f"AI Request Failed. {e.__class__.__name__}: {e}") from e

    async def _generate_image_openai(self, prompt: str) -> bytes | None:
        """Generate an image using DALL-E 3 with Google AI watermark (Internal OpenAI impl)"""
        # Note: Keeps 'Google AI watermark' legacy name/comment if that's what it was
        
        if not self.enable_image_services:
            self.logger.warning("OpenAI image services are disabled")
            return None

        try:
            from mealie.pkgs.img.watermark import apply_watermark
            
            client = self.get_client()
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                response_format="b64_json",
            )

            if not response.data:
                return None

            image_data = response.data[0].b64_json
            if not image_data:
                return None

            image_bytes = base64.b64decode(image_data)
            
            # Apply watermark to all AI-generated images
            try:
                watermarked_bytes = apply_watermark(image_bytes)
                return watermarked_bytes
            except Exception as e:
                self.logger.warning(f"Failed to apply watermark, returning original image: {e}")
                return image_bytes

        except Exception as e:
            self.logger.error(f"Failed to generate image: {e}")
            return None

    async def generate_image(self, prompt: str) -> bytes | None:
        return await self.provider.generate_image(prompt)
