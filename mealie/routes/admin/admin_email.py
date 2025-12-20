from typing import Annotated

from fastapi import APIRouter, Header

from mealie.routes._base import BaseAdminController, controller
from mealie.schema.admin.email import EmailReady, EmailSuccess, EmailTest
from mealie.schema.admin.email import EmailReady, EmailSuccess, EmailTest
from mealie.services.email import EmailService
from mealie.services.admin.settings_service import SettingsService

router = APIRouter(prefix="/email")


@controller(router)
class AdminEmailController(BaseAdminController):
    @router.get("", response_model=EmailReady)
    async def check_email_config(self):
        """Get general application information"""
        # Logic duplicated from EmailService._is_smtp_enabled for now, or we can instantiate service
        config = SettingsService(self.session).get_effective_smtp_settings()
        ready = bool(config.get("SMTP_HOST") and config.get("SMTP_PORT"))
        return EmailReady(ready=ready)

    @router.post("", response_model=EmailSuccess)
    async def send_test_email(
        self,
        data: EmailTest,
        accept_language: Annotated[str | None, Header()] = None,
    ):
        service = EmailService(locale=accept_language, session=self.session)
        status = False
        error = None

        try:
            status = service.send_test_email(data.email)
        except Exception as e:
            self.logger.error(e)
            error = str(e)

        return EmailSuccess(success=status, error=error)
