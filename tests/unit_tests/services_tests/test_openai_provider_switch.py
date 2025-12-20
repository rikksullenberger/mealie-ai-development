import pytest
from mealie.services.admin.settings_service import SettingsService
from mealie.schema.admin.site_settings import SiteSettingsIn
from mealie.services.openai.openai import OpenAIService
from mealie.services.openai.providers import OpenAIProvider, GoogleAIProvider
from mealie.core.config import get_app_settings

# Mocking Google API import if needed or depending on try/except block
# tests usually run in environment where deps might be missing?
# The `providers.py` handles missing dep by logging error but class exists.

def test_provider_init_default_openai(db_session):
    # Default settings (provider=openai, key=None)
    service = OpenAIService(db_session)
    assert isinstance(service.provider, OpenAIProvider)
    assert service.ai_provider == "openai"

def test_provider_switch_to_google(db_session):
    settings_service = SettingsService(db_session)
    settings_service.update_settings(SiteSettingsIn(
        ai_provider="google",
        google_api_key="test-google-key",
        google_model="gemini-pro"
    ))
    
    service = OpenAIService(db_session)
    assert isinstance(service.provider, GoogleAIProvider)
    assert service.ai_provider == "google"
    assert service.google_api_key == "test-google-key"

def test_provider_fallback_if_google_key_missing(db_session):
    settings_service = SettingsService(db_session)
    settings_service.update_settings(SiteSettingsIn(
        ai_provider="google",
        google_api_key=None, # Explicitly no key
    ))
    
    # Ensure env var is also empty (might be leaking from other tests or env)
    # But SettingsService merge logic handles it. Just ensure DB has google but no key.
    
    service = OpenAIService(db_session)
    # Should fallback to OpenAIProvider
    assert isinstance(service.provider, OpenAIProvider)
