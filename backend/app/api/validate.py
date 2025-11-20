from fastapi import APIRouter
from ..schemas import ValidateRequest, ValidateResponse
from ..services.validators import mikrotik

router = APIRouter()

@router.post('/validate', response_model=ValidateResponse)
def validate_config(request: ValidateRequest):
    vendor = request.vendor.lower()

    if vendor == 'mikrotik':
        issues = mikrotik.validate_config(request.config)
    else:
        issues = ['Vendor no soportado para validación']
    return ValidateResponse(ok=len(issues) == 0, issues=issues)
