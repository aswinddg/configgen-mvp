from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.models import Scenario, Vendor
from ..schemas import GenerateRequest
from ..services.templating import render_template
from ..services.validators import mikrotik
import unicodedata
import re

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
    if scenario.name == "WAN IP Estática" or scenario.name == "Configuración Modular":
        if vendor.name == "Mikrotik":
            template_path = "mikrotik/generic.j2"
            file_extension = "rsc"
        elif vendor.name == "Cisco":
            template_path = "cisco/generic.j2"
            file_extension = "txt"
        elif vendor.name == "Juniper":
            template_path = "junos/generic.j2"
            file_extension = "conf"
        else:
            raise HTTPException(status_code=400, detail="Vendor no soportado para este scenario")
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
        def sanitize_filename(name):
            # Normalize unicode characters (e.g. á -> a)
            name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
            # Replace spaces with underscores and remove non-alphanumeric
            name = re.sub(r'[^\w\s-]', '', name).strip().lower()
            return re.sub(r'[-\s]+', '_', name)

        safe_scenario_name = sanitize_filename(scenario.name)
        filename = f"{vendor.name.lower()}_{safe_scenario_name}.{file_extension}"
        
        return Response(
            content=config_content,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando configuración: {str(e)}")