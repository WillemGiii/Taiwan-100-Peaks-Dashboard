"""Pandas cleaning pipeline for HikingNote records."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import pandas as pd


HIKING_RECORD_COLUMNS = [
    "trail_name",
    "distance_km",
    "ascent_m",
    "descent_m",
    "duration_minutes",
    "record_date",
]

DEDUPLICATION_COLUMNS = [
    "trail_name",
    "distance_km",
    "ascent_m",
    "descent_m",
    "duration_minutes",
    "record_date",
]


@dataclass(frozen=True)
class CleaningSummary:
    raw_count: int
    cleaned_count: int
    removed_count: int
    trail_counts: dict[str, int]


def _parse_number(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None

    text = str(value).strip().replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None

    return float(match.group(0))


def _parse_int(value: Any) -> int | None:
    number = _parse_number(value)
    if number is None:
        return None

    return int(round(number))


def clean_hiking_records(raw_records: list[dict[str, Any]]) -> pd.DataFrame:
    """Clean raw HikingNote records into the hiking_records table shape."""

    raw_count = len(raw_records)
    df = pd.DataFrame(raw_records)

    if df.empty:
        empty_df = pd.DataFrame(columns=HIKING_RECORD_COLUMNS)
        empty_df.attrs["summary"] = CleaningSummary(
            raw_count=raw_count,
            cleaned_count=0,
            removed_count=raw_count,
            trail_counts={},
        )
        return empty_df

    for column in HIKING_RECORD_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    df = df[HIKING_RECORD_COLUMNS].copy()
    df["trail_name"] = df["trail_name"].astype("string").str.strip()
    df["distance_km"] = df["distance_km"].map(_parse_number).round(2)
    df["ascent_m"] = df["ascent_m"].map(_parse_int).astype("Int64")
    df["descent_m"] = df["descent_m"].map(_parse_int).astype("Int64")
    df["duration_minutes"] = df["duration_minutes"].map(_parse_int).astype("Int64")
    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce").dt.date

    valid_mask = (
        df["trail_name"].notna()
        & (df["trail_name"].str.len() > 0)
        & df["duration_minutes"].notna()
        & (df["duration_minutes"] > 0)
        & df["record_date"].notna()
    )
    df = df.loc[valid_mask].copy()
    df = df.drop_duplicates(subset=DEDUPLICATION_COLUMNS).reset_index(drop=True)

    trail_counts = df["trail_name"].value_counts().sort_index().to_dict()
    cleaned_count = len(df)
    df.attrs["summary"] = CleaningSummary(
        raw_count=raw_count,
        cleaned_count=cleaned_count,
        removed_count=raw_count - cleaned_count,
        trail_counts={str(key): int(value) for key, value in trail_counts.items()},
    )

    return df


def print_cleaning_summary(df: pd.DataFrame) -> None:
    summary = df.attrs.get("summary")
    if not isinstance(summary, CleaningSummary):
        print("清洗摘要不存在。")
        return

    print("\n清洗摘要")
    print("-" * 40)
    print(f"原始筆數: {summary.raw_count}")
    print(f"清洗後筆數: {summary.cleaned_count}")
    print(f"被移除筆數: {summary.removed_count}")
    print("各 trail_name 筆數:")
    if not summary.trail_counts:
        print("  無")
        return

    for trail_name, count in summary.trail_counts.items():
        print(f"  {trail_name}: {count}")

