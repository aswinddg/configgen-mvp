from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.models import Scenario, Vendor
from ..schemas import GenerateRequest
from ..services.templating import render_template
from ..services.validators import mikrotik

router = APIRouter()

@router.post("/generate")
async def generate_config(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    # Obtener scenario y vendor
    result = await db.execute(
        select(Scenario, Vendor)
        .join(Vendor)
        .where(Scenario.id == request.scenario_id)
    )
    scenario_vendor = result.first()
    
    if not scenario_vendor:
        raise HTTPException(status_code=404, detail="Scenario no encontrado")
    
    scenario, vendor = scenario_vendor
    
    # Determinar template path basado en scenario
    if scenario.name == "WAN IP Estática" and vendor.name == "Mikrotik":
        template_path = "mikrotik/wan/static_ip.j2"
        file_extension = "rsc"
    else:
        raise HTTPException(status_code=400, detail="Template no disponible para este scenario")
    
    try:
        # Generar configuración
        config_content = render_template(template_path, request.params)

        # Validar configuración generada
        if vendor.name == "Mikrotik":
            config_issues = mikrotik.validate_config(config_content)
            if config_issues:
                raise HTTPException(status_code=500, detail=f"Configuración generada inválida: {', '.join(config_issues)}")
        
        # Retornar como archivo descargable
        filename = f"{vendor.name.lower()}_{scenario.name.replace(' ', '_').lower()}.{file_extension}"
        
        return Response(
            content=config_content,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando configuración: {str(e)}")