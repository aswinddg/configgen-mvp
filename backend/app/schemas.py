from pydantic import BaseModel
from typing import List, Dict, Any

class VendorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ScenarioResponse(BaseModel):
    id: int
    vendor_id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class ParamResponse(BaseModel):
    id: int
    scenario_id: int
    key: str
    label: str
    type: str
    required: bool
    default_value: str
    options: str | None = None

    class Config:
        from_attributes = True

class GenerateRequest(BaseModel):
    scenario_id: int
    params: Dict[str, Any]

class ValidateRequest(BaseModel):
    vendor: str
    config: str

class ValidateResponse(BaseModel):
    ok: bool
    issues: List[str] = []    