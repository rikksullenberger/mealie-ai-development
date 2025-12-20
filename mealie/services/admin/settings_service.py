from sqlalchemy.orm import Session

from mealie.core.config import get_app_settings
from mealie.db.models.server.settings import SiteSettings
from mealie.schema.admin.site_settings import SiteSettingsIn


class SettingsService:
    def __init__(self, session: Session):
        self.session = session
        self.app_settings = get_app_settings()

    def get_settings(self) -> SiteSettings:
        return SiteSettings.get_settings(self.session)

    def update_settings(self, data: SiteSettingsIn) -> SiteSettings:
        settings = self.get_settings()
        
        update_data = data.model_dump(exclude_unset=True)
        
        # Handle secrets: if the value is "*****", it means "unchanged", so we shouldn't update it
        # But wait, the frontend sends the masked value? 
        # Usually, if frontend sends "*****", we ignore it. If it sends a new string, we update.
        # However, SiteSettingsIn doesn't use MaskedString, it just expects string.
        # If the user doesn't touch the field, the frontend might send null or the masked value.
        # A safer approach for updates usually is: 
        # - If value is None => don't update (if patch) OR set to None (if replace)?
        # - If value is "*****" => ignore.
        
        for key, value in update_data.items():
            if value == "*****":
                continue
            setattr(settings, key, value)

        self.session.commit()
        self.session.refresh(settings)
        return settings

    def get_effective_openai_api_key(self) -> str | None:
        db_settings = self.get_settings()
        if db_settings.openai_api_key:
            return db_settings.openai_api_key
        return self.app_settings.OPENAI_API_KEY
        
    def get_effective_openai_model(self) -> str:
        db_settings = self.get_settings()
        if db_settings.openai_model:
            return db_settings.openai_model
        return self.app_settings.OPENAI_MODEL
        return self.app_settings.OPENAI_MODEL

    def get_effective_ai_provider(self) -> str:
        db_settings = self.get_settings()
        if db_settings.ai_provider:
            return db_settings.ai_provider
        return "openai"

    def get_effective_google_api_key(self) -> str | None:
        db_settings = self.get_settings()
        if db_settings.google_api_key:
            return db_settings.google_api_key
        return self.app_settings.GOOGLE_API_KEY

    def get_effective_google_model(self) -> str:
        db_settings = self.get_settings()
        if db_settings.google_model:
            return db_settings.google_model
        return self.app_settings.GOOGLE_MODEL
        db_settings = self.get_settings()
        # Merge logic: DB > Env
        # This is a bit complex because we need to return an object compatible with email service
        # or just a dict of settings.
        
        return {
            "SMTP_HOST": db_settings.smtp_host or self.app_settings.SMTP_HOST,
            "SMTP_PORT": db_settings.smtp_port or self.app_settings.SMTP_PORT,
            "SMTP_USER": db_settings.smtp_user or self.app_settings.SMTP_USER,
            "SMTP_PASSWORD": db_settings.smtp_password or self.app_settings.SMTP_PASSWORD,
            "SMTP_FROM_NAME": db_settings.smtp_from_name or self.app_settings.SMTP_FROM_NAME,
            "SMTP_FROM_EMAIL": db_settings.smtp_from_email or self.app_settings.SMTP_FROM_EMAIL,
            "SMTP_AUTH_STRATEGY": db_settings.smtp_auth_strategy or self.app_settings.SMTP_AUTH_STRATEGY,
        }
