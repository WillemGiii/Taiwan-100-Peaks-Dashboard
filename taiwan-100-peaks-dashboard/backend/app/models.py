"""SQLAlchemy ORM models for mountain routes and HikingNote records."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Identity, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class Mountain(Base):
    """Mountain and trail metadata used by the map and API."""

    __tablename__ = "mountains"

    hiking_note_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=False,
    )
    ch_mt_name: Mapped[str] = mapped_column(String(100), nullable=False)
    ch_trail_name: Mapped[str] = mapped_column(String(150), nullable=False)
    longitude_wgs84: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    latitude_wgs84: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    trail_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    length_km: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    elevation_min_m: Mapped[int | None] = mapped_column(Integer)
    elevation_max_m: Mapped[int | None] = mapped_column(Integer)
    elevation_diff_m: Mapped[int | None] = mapped_column(Integer)
    country_raw: Mapped[str | None] = mapped_column(Text)

    records: Mapped[list["HikingRecord"]] = relationship(back_populates="mountain")


class HikingRecord(Base):
    """Raw HikingNote hiking record for dashboard aggregation."""

    __tablename__ = "hiking_records"

    id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True)
    trail_name: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("mountains.trail_name"),
        nullable=False,
    )
    distance_km: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    ascent_m: Mapped[int | None] = mapped_column(Integer)
    descent_m: Mapped[int | None] = mapped_column(Integer)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    record_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )

    mountain: Mapped[Mountain] = relationship(back_populates="records")
