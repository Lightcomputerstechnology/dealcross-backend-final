from pydantic import BaseModel
from typing import Optional

class AppSettings(BaseModel):
    maintenance_mode: bool
    site_name: str
    support_email: Optional[str] = None

    model_config = {"from_attributes": True}
