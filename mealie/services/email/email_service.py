from pathlib import Path
from sqlalchemy.orm import Session
from mealie.db.db_setup import session_context
from mealie.services.admin.settings_service import SettingsService

from jinja2 import Template
from pydantic import BaseModel

from mealie.core.root_logger import get_logger
from mealie.lang import local_provider
from mealie.lang.providers import Translator
from mealie.services._base_service import BaseService

from .email_senders import ABCEmailSender, DefaultEmailSender

CWD = Path(__file__).parent

logger = get_logger()


class EmailTemplate(BaseModel):
    subject: str
    header_text: str
    message_top: str
    message_bottom: str
    button_link: str
    button_text: str

    def render_html(self, template: Path) -> str:
        tmpl = Template(template.read_text())

        return tmpl.render(data=self.model_dump())


class EmailService(BaseService):
    def __init__(self, sender: ABCEmailSender | None = None, locale: str | None = None, session: Session | None = None) -> None:
        self.templates_dir = CWD / "templates"
        self.default_template = self.templates_dir / "default.html"
        # If sender is provided, we assume it's already configured or doesn't need our session.
        # But if we create DefaultEmailSender, pass the session.
        self.sender: ABCEmailSender = sender or DefaultEmailSender(session=session)
        self.translator: Translator = local_provider(locale)
        self.session = session

        super().__init__()

    def _is_smtp_enabled(self) -> bool:
        # Check if enabled dynamically
        # Since SettingsService handles merging, we just check if required fields are present?
        # AppSettings.SMTP_ENABLE checks self.SMTP_FEATURE.enabled.
        # We need similar logic on the effective settings.
        
        def get_check(sess: Session):
             config = SettingsService(sess).get_effective_smtp_settings()
             # Simplified check: HOST and PORT must be set
             return bool(config.get("SMTP_HOST") and config.get("SMTP_PORT"))

        if self.session:
            return get_check(self.session)
        else:
            with session_context() as sess:
                return get_check(sess)

    def send_email(self, email_to: str, data: EmailTemplate) -> bool:
        if not self._is_smtp_enabled():
            return False

        return self.sender.send(email_to, data.subject, data.render_html(self.default_template))

    def send_forgot_password(self, address: str, reset_password_url: str) -> bool:
        forgot_password = EmailTemplate(
            subject=self.translator.t("emails.password.subject"),
            header_text=self.translator.t("emails.password.header_text"),
            message_top=self.translator.t("emails.password.message_top"),
            message_bottom=self.translator.t("emails.password.message_bottom"),
            button_link=reset_password_url,
            button_text=self.translator.t("emails.password.button_text"),
        )
        return self.send_email(address, forgot_password)

    def send_invitation(self, address: str, invitation_url: str) -> bool:
        invitation = EmailTemplate(
            subject=self.translator.t("emails.invitation.subject"),
            header_text=self.translator.t("emails.invitation.header_text"),
            message_top=self.translator.t("emails.invitation.message_top"),
            message_bottom=self.translator.t("emails.invitation.message_bottom"),
            button_link=invitation_url,
            button_text=self.translator.t("emails.invitation.button_text"),
        )
        return self.send_email(address, invitation)

    def send_test_email(self, address: str) -> bool:
        test_email = EmailTemplate(
            subject=self.translator.t("emails.test.subject"),
            header_text=self.translator.t("emails.test.header_text"),
            message_top=self.translator.t("emails.test.message_top"),
            message_bottom=self.translator.t("emails.test.message_bottom"),
            button_link=self.settings.BASE_URL,
            button_text=self.translator.t("emails.test.button_text"),
        )
        return self.send_email(address, test_email)
