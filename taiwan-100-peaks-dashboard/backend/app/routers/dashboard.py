"""Mountain dashboard statistics API routes."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Integer, cast, extract, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HikingRecord, Mountain
from app.schemas import DashboardResponse, MonthlyDistribution


INSUFFICIENT_DATA_MESSAGE = "目前此山岳登山紀錄不足，暫時無法產生可靠統計。"

router = APIRouter(prefix="/api/mountains", tags=["dashboard"])


def _to_float(value: Decimal | int | float | None) -> float | None:
    return round(float(value), 2) if value is not None else None


def _empty_dashboard_response(mountain: Mountain) -> DashboardResponse:
    return DashboardResponse(
        mountain_id=mountain.hiking_note_id,
        mountain_name=mountain.ch_trail_name,
        trail_name=mountain.trail_name,
        average_duration_minutes=None,
        average_distance_km=None,
        average_ascent_m=None,
        average_descent_m=None,
        monthly_distribution=[],
        data_status="insufficient_data",
        message=INSUFFICIENT_DATA_MESSAGE,
    )


@router.get("/{mountain_id}/dashboard", response_model=DashboardResponse)
def get_mountain_dashboard(
    mountain_id: int,
    db: Session = Depends(get_db),
) -> DashboardResponse:
    mountain = db.get(Mountain, mountain_id)
    if mountain is None:
        raise HTTPException(status_code=404, detail="Mountain not found.")

    stats = db.execute(
        select(
            func.count(HikingRecord.id),
            func.avg(HikingRecord.duration_minutes),
            func.avg(HikingRecord.distance_km),
            func.avg(HikingRecord.ascent_m),
            func.avg(HikingRecord.descent_m),
        ).where(HikingRecord.trail_name == mountain.trail_name)
    ).one()

    record_count = int(stats[0] or 0)
    if record_count == 0:
        return _empty_dashboard_response(mountain)

    month_expr = cast(extract("month", HikingRecord.record_date), Integer)
    month_rows = db.execute(
        select(month_expr.label("month"), func.count(HikingRecord.id).label("count"))
        .where(
            HikingRecord.trail_name == mountain.trail_name,
            HikingRecord.record_date.is_not(None),
        )
        .group_by(month_expr)
        .order_by(month_expr)
    ).all()
    month_counts = {int(row.month): int(row.count) for row in month_rows}

    return DashboardResponse(
        mountain_id=mountain.hiking_note_id,
        mountain_name=mountain.ch_trail_name,
        trail_name=mountain.trail_name,
        average_duration_minutes=_to_float(stats[1]),
        average_distance_km=_to_float(stats[2]),
        average_ascent_m=_to_float(stats[3]),
        average_descent_m=_to_float(stats[4]),
        monthly_distribution=[
            MonthlyDistribution(month=month, count=month_counts.get(month, 0))
            for month in range(1, 13)
        ],
        data_status="ok",
    )

