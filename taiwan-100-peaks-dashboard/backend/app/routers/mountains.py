"""Mountain metadata API routes."""

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Mountain
from app.schemas import MountainResponse


router = APIRouter(prefix="/api/mountains", tags=["mountains"])


def _to_float(value: Decimal | None) -> float | None:
    return float(value) if value is not None else None


def _mountain_response(mountain: Mountain) -> MountainResponse:
    return MountainResponse(
        hiking_note_id=mountain.hiking_note_id,
        ch_mt_name=mountain.ch_mt_name,
        ch_trail_name=mountain.ch_trail_name,
        trail_name=mountain.trail_name,
        latitude=_to_float(mountain.latitude_wgs84),
        longitude=_to_float(mountain.longitude_wgs84),
        length_km=float(mountain.length_km),
        elevation=mountain.elevation_diff_m,
        elevation_min_m=mountain.elevation_min_m,
        elevation_max_m=mountain.elevation_max_m,
        country=mountain.country_raw,
    )


@router.get("", response_model=list[MountainResponse])
def list_mountains(db: Session = Depends(get_db)) -> list[MountainResponse]:
    mountains = db.execute(
        select(Mountain).order_by(Mountain.hiking_note_id)
    ).scalars().all()
    return [_mountain_response(mountain) for mountain in mountains]

