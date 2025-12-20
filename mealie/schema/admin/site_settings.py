from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer

MaskedString = Annotated[
    str | None,
    PlainSerializer(lambda x: None if x is None else "*****", return_type=str | None),
]


class SiteSettingsBase(BaseModel):
    ai_provider: str | None = None
    openai_api_key: str | None = None
    openai_model: str | None = None
    openai_base_url: str | None = None

    google_api_key: str | None = None
    google_model: str | None = None

    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from_name: str | None = None
    smtp_from_email: str | None = None
    smtp_auth_strategy: str | None = None


class SiteSettingsIn(SiteSettingsBase):
    pass


class SiteSettingsOut(SiteSettingsBase):
    openai_api_key: MaskedString = None
    google_api_key: MaskedString = None
    smtp_user: MaskedString = None
    smtp_password: MaskedString = None

    model_config = ConfigDict(from_attributes=True)
