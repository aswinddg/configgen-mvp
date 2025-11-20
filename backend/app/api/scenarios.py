from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.models import Scenario, Vendor
from ..schemas import ScenarioResponse
from typing import List, Optional

router = APIRouter()

@router.get("/scenarios", response_model=List[ScenarioResponse])
async def get_scenarios(
    vendor: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Scenario)
    if vendor:
        # Filtrar por nombre de vendor
        query = query.join(Vendor).where(Vendor.name.ilike(f"%{vendor}%"))

    result = await db.execute(query)
    scenarios = result.scalars().all()
    return scenarios
