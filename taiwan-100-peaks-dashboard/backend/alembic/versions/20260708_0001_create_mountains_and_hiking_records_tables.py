"""create mountains and hiking records tables

Revision ID: 20260708_0001
Revises:
Create Date: 2026-07-08 12:00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260708_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "mountains",
        sa.Column(
            "hiking_note_id",
            sa.Integer(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("ch_mt_name", sa.String(length=100), nullable=False),
        sa.Column("ch_trail_name", sa.String(length=150), nullable=False),
        sa.Column("longitude_wgs84", sa.Numeric(10, 7), nullable=True),
        sa.Column("latitude_wgs84", sa.Numeric(10, 7), nullable=True),
        sa.Column("trail_name", sa.String(length=100), nullable=False),
        sa.Column("length_km", sa.Numeric(6, 2), nullable=False),
        sa.Column("elevation_min_m", sa.Integer(), nullable=True),
        sa.Column("elevation_max_m", sa.Integer(), nullable=True),
        sa.Column("elevation_diff_m", sa.Integer(), nullable=True),
        sa.Column("country_raw", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("hiking_note_id", name=op.f("pk_mountains")),
        sa.UniqueConstraint("trail_name", name="uq_mountains_trail_name"),
    )

    op.create_table(
        "hiking_records",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=False),
            nullable=False,
        ),
        sa.Column("trail_name", sa.String(length=100), nullable=False),
        sa.Column("distance_km", sa.Numeric(6, 2), nullable=True),
        sa.Column("ascent_m", sa.Integer(), nullable=True),
        sa.Column("descent_m", sa.Integer(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("record_date", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["trail_name"],
            ["mountains.trail_name"],
            name="fk_hiking_records_trail_name_mountains",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_hiking_records")),
    )


def downgrade() -> None:
    op.drop_table("hiking_records")
    op.drop_table("mountains")
