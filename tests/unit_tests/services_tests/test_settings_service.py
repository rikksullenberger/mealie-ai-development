import pytest
from mealie.services.admin.settings_service import SettingsService
from mealie.schema.admin.site_settings import SiteSettingsIn
from mealie.core.config import get_app_settings

def test_settings_service_defaults(db_session):
    service = SettingsService(db_session)
    settings = service.get_settings()
    assert settings.id == 1
    assert settings.openai_api_key is None

def test_settings_update(db_session):
    service = SettingsService(db_session)
    update_data = SiteSettingsIn(openai_api_key="sk-test-key", openai_model="gpt-4")
    updated = service.update_settings(update_data)
    
    assert updated.openai_api_key == "sk-test-key"
    assert updated.openai_model == "gpt-4"
    
    # Verify persistence
    # We might need to refresh or use a new service instance
    db_session.expire_all()
    service2 = SettingsService(db_session)
    fetched = service2.get_settings()
    assert fetched.openai_api_key == "sk-test-key"

def test_effective_settings_merge(db_session, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    monkeypatch.setenv("OPENAI_MODEL", "env-model")
    
    # Reload app settings to pick up env vars
    get_app_settings.cache_clear()
    
    service = SettingsService(db_session)
    
    # Before update: use env (DB is empty/nulls)
    assert service.get_effective_openai_api_key() == "env-key"
    assert service.get_effective_openai_model() == "env-model"
    
    # Update DB
    service.update_settings(SiteSettingsIn(openai_api_key="db-key"))
    
    # After update: use DB for key, Env for model (since DB model is None)
    assert service.get_effective_openai_api_key() == "db-key"
    assert service.get_effective_openai_model() == "env-model"

    # Update DB model
    service.update_settings(SiteSettingsIn(openai_model="db-model"))
    assert service.get_effective_openai_model() == "db-model"


def test_google_settings_merge(db_session, monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "env-google-key")
    monkeypatch.setenv("GOOGLE_MODEL", "env-gemini")
    
    get_app_settings.cache_clear()
    
    service = SettingsService(db_session)
    
    # Defaults
    assert service.get_effective_ai_provider() == "openai"
    assert service.get_effective_google_api_key() == "env-google-key"
    assert service.get_effective_google_model() == "env-gemini"
    
    # Update
    service.update_settings(SiteSettingsIn(ai_provider="google", google_api_key="db-google-key"))
    assert service.get_effective_ai_provider() == "google"
    assert service.get_effective_google_api_key() == "db-google-key"
