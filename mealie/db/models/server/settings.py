from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from mealie.db.models._model_base import SqlAlchemyBase


class SiteSettings(SqlAlchemyBase):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, default=1)

    # AI Provider
    ai_provider = Column(String, default="openai")  # openai, google

    # OpenAI
    openai_api_key = Column(String, nullable=True)
    openai_model = Column(String, default="gpt-3.5-turbo")
    openai_base_url = Column(String, nullable=True)

    # Google
    google_api_key = Column(String, nullable=True)
    google_model = Column(String, default="gemini-pro")

    # SMTP Settings
    smtp_host = Column(String, nullable=True)
    smtp_port = Column(Integer, nullable=True)
    smtp_user = Column(String, nullable=True)
    smtp_password = Column(String, nullable=True)
    smtp_from_name = Column(String, nullable=True)
    smtp_from_email = Column(String, nullable=True)
    smtp_auth_strategy = Column(String, nullable=True)

    @classmethod
    def get_settings(cls, session: Session) -> "SiteSettings":
        settings = session.query(cls).filter_by(id=1).first()
        if not settings:
            settings = cls(id=1)
            session.add(settings)
            session.commit()
        return settings
