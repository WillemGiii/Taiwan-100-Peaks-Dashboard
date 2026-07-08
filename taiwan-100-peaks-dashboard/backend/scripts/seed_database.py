"""Load MVP seed data into PostgreSQL."""

from pathlib import Path

from sqlalchemy import create_engine

from app.database import DATABASE_URL


def split_sql_statements(sql: str) -> list[str]:
    return [statement.strip() for statement in sql.split(";") if statement.strip()]


def main() -> None:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is required to seed the database.")

    seed_path = Path(__file__).resolve().parents[2] / "db" / "seed.sql"
    seed_sql = seed_path.read_text(encoding="utf-8")

    engine = create_engine(DATABASE_URL, future=True)
    with engine.begin() as connection:
        for statement in split_sql_statements(seed_sql):
            connection.exec_driver_sql(statement)

    print(f"Loaded seed data from {seed_path}")


if __name__ == "__main__":
    main()
