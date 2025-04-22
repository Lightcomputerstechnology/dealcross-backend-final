# File: schemas/config_schema.py

from pydantic import BaseModel

class ConfigOut(BaseModel):
    key: str
    value: str

    model_config = {"from_attributes": True}
