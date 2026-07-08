"""Load cleaned HikingNote records into PostgreSQL."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import bindparam, create_engine, text
from sqlalchemy.engine import Engine


@dataclass(frozen=True)
class LoadSummary:
    attempted_count: int
    inserted_count: int
    skipped_count: int
    skipped_trail_names: list[str]
    deleted_count: int


def load_environment() -> None:
    crawler_dir = Path(__file__).resolve().parent
    project_dir = crawler_dir.parent

    load_dotenv(project_dir / ".env")
    load_dotenv(crawler_dir / ".env")
    load_dotenv()


def get_database_url() -> str:
    load_environment()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required to load hiking records.")
    return database_url


def create_postgres_engine(database_url: str | None = None) -> Engine:
    return create_engine(database_url or get_database_url(), future=True)


def _records_for_insert(df: pd.DataFrame) -> list[dict[str, Any]]:
    records = df[
        [
            "trail_name",
            "distance_km",
            "ascent_m",
            "descent_m",
            "duration_minutes",
            "record_date",
        ]
    ].copy()

    records = records.astype(object).where(pd.notna(records), None)
    return records.to_dict(orient="records")


def load_hiking_records_to_postgres(
    clean_df: pd.DataFrame,
    database_url: str | None = None,
) -> LoadSummary:
    """Replace current hiking_records for fetched trails with cleaned records.

    MVP replace strategy: within one transaction, delete existing hiking_records
    for trail_name values present in this run, then insert the cleaned records.
    This avoids duplicate imports without changing the database schema.
    """

    attempted_count = len(clean_df)
    if clean_df.empty:
        return LoadSummary(
            attempted_count=attempted_count,
            inserted_count=0,
            skipped_count=0,
            skipped_trail_names=[],
            deleted_count=0,
        )

    engine = create_postgres_engine(database_url)

    with engine.begin() as connection:
        valid_trail_names = {
            row[0]
            for row in connection.execute(text("SELECT trail_name FROM mountains"))
        }

        incoming_trail_names = set(clean_df["trail_name"].dropna().astype(str))
        skipped_trail_names = sorted(incoming_trail_names - valid_trail_names)

        load_df = clean_df[clean_df["trail_name"].isin(valid_trail_names)].copy()
        skipped_count = attempted_count - len(load_df)

        if load_df.empty:
            return LoadSummary(
                attempted_count=attempted_count,
                inserted_count=0,
                skipped_count=skipped_count,
                skipped_trail_names=skipped_trail_names,
                deleted_count=0,
            )

        trail_names_to_replace = sorted(load_df["trail_name"].unique().tolist())
        delete_stmt = text(
            "DELETE FROM hiking_records WHERE trail_name IN :trail_names"
        ).bindparams(bindparam("trail_names", expanding=True))
        delete_result = connection.execute(
            delete_stmt,
            {"trail_names": trail_names_to_replace},
        )

        insert_stmt = text(
            """
            INSERT INTO hiking_records (
                trail_name,
                distance_km,
                ascent_m,
                descent_m,
                duration_minutes,
                record_date
            ) VALUES (
                :trail_name,
                :distance_km,
                :ascent_m,
                :descent_m,
                :duration_minutes,
                :record_date
            )
            """
        )
        payload = _records_for_insert(load_df)
        connection.execute(insert_stmt, payload)

    return LoadSummary(
        attempted_count=attempted_count,
        inserted_count=len(payload),
        skipped_count=skipped_count,
        skipped_trail_names=skipped_trail_names,
        deleted_count=delete_result.rowcount if delete_result.rowcount is not None else 0,
    )


def print_load_summary(summary: LoadSummary) -> None:
    print("\n資料庫載入摘要")
    print("-" * 40)
    print(f"嘗試寫入筆數: {summary.attempted_count}")
    print(f"實際寫入筆數: {summary.inserted_count}")
    print(f"略過筆數: {summary.skipped_count}")
    print(f"取代前刪除舊資料筆數: {summary.deleted_count}")

    if summary.skipped_trail_names:
        print("略過 trail_name:")
        for trail_name in summary.skipped_trail_names:
            print(f"  {trail_name}")

