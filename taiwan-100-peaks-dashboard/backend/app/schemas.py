"""Pydantic response schemas for the backend API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class MountainResponse(BaseModel):
    hiking_note_id: int
    ch_mt_name: str
    ch_trail_name: str
    trail_name: str
    latitude: float | None
    longitude: float | None
    length_km: float
    elevation: int | None
    elevation_min_m: int | None
    elevation_max_m: int | None
    country: str | None

    model_config = ConfigDict(from_attributes=True)


class MonthlyDistribution(BaseModel):
    month: int
    count: int


class DashboardResponse(BaseModel):
    mountain_id: int
    mountain_name: str
    trail_name: str
    average_duration_minutes: float | None
    average_distance_km: float | None
    average_ascent_m: float | None
    average_descent_m: float | None
    monthly_distribution: list[MonthlyDistribution]
    data_status: Literal["ok", "insufficient_data"]
    message: str | None = None

