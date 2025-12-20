from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mealie.core.dependencies import get_db
from mealie.routes._base import BaseAdminController, controller
from mealie.schema.admin.site_settings import SiteSettings, SiteSettingsIn, SiteSettingsOut
from mealie.services.admin.settings_service import SettingsService

router = APIRouter(prefix="/detailed-settings")

@controller(router)
class AdminSiteSettingsController(BaseAdminController):
    
    @router.get("", response_model=SiteSettingsOut)
    async def get_settings(self, db: Session = Depends(get_db)):
        return SettingsService(db).get_settings()

    @router.put("", response_model=SiteSettingsOut)
    async def update_settings(self, data: SiteSettingsIn, db: Session = Depends(get_db)):
        service = SettingsService(db)
        return service.update_settings(data)
