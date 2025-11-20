from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.models import Vendor
from ..schemas import VendorResponse
from typing import List

router = APIRouter()

@router.get("/vendors", response_model=List[VendorResponse])
async def get_vendors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vendor))
    vendors = result.scalars().all()
    return vendors
