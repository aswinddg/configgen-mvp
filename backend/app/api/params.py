from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.models import Param
from ..schemas import ParamResponse
from typing import List

router = APIRouter()

@router.get("/scenarios/{scenario_id}/params", response_model=List[ParamResponse])
async def get_scenario_params(
    scenario_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Param).where(Param.scenario_id == scenario_id)
    )
    params = result.scalars().all()
    
    if not params:
        raise HTTPException(status_code=404, detail="No se encontraron parámetros para este scenario")
    
    return params