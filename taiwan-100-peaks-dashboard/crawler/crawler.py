"""Scrape, clean, and load HikingNote records into PostgreSQL."""

from pathlib import Path

from dotenv import load_dotenv


CRAWLER_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CRAWLER_DIR.parent

load_dotenv(PROJECT_DIR / ".env")
load_dotenv(CRAWLER_DIR / ".env")
load_dotenv()

from data_cleaning import clean_hiking_records, print_cleaning_summary
from hiking_note_scraper import TRAIL_DATA, scrape_all_trails
from load_to_db import load_hiking_records_to_postgres, print_load_summary


def main() -> None:
    print("開始抓取 HikingNote 公開登山紀錄...")
    raw_records = scrape_all_trails(TRAIL_DATA, max_pages=9)

    clean_df = clean_hiking_records(raw_records)
    print_cleaning_summary(clean_df)

    load_summary = load_hiking_records_to_postgres(clean_df)
    print_load_summary(load_summary)

    print("\n匯入流程完成。")


if __name__ == "__main__":
    main()
