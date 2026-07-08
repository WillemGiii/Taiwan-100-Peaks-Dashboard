# Taiwan 100 Peaks One-Day Hike Dashboard

臺灣百岳單攻資料視覺化專案。MVP 目標是用地圖呈現可單攻百岳，並在後續透過 FastAPI、PostgreSQL 與既有 HikingNote 爬蟲資料提供統計儀表板。

## 專案結構

```text
taiwan-100-peaks-dashboard/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── peaks.py
│   │       └── stats.py
│   ├── pyproject.toml
│   └── uv.lock
├── crawler/
│   ├── hiking_note_scraper.py
│   ├── pyproject.toml
│   └── uv.lock
├── db/
│   ├── init.sql
│   └── seed.sql
├── docs/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── PROJECT_CONTEXT.md
```

## Backend

Backend 是獨立 uv 專案，位於 `backend/`。

```powershell
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

目前只建立 FastAPI placeholder，尚未實作正式 API endpoint。

## Crawler

Crawler 是獨立 uv 專案，位於 `crawler/`。既有爬蟲程式已保留在：

```text
crawler/hiking_note_scraper.py
```

執行方式：

```powershell
cd crawler
uv sync
$env:HIKING_NOTE_COOKIE="name=value; another_name=another_value"
uv run python hiking_note_scraper.py
```

本專案已存在 HikingNote 爬蟲邏輯；除非任務明確要求，不要重寫 `hiking_note_scraper.py` 的核心爬蟲、解析與分頁邏輯。
若爬蟲需要 Cookie，請透過 `HIKING_NOTE_COOKIE` 環境變數提供，不要寫死在程式碼中。

## Python 套件管理規則

- Python dependencies 一律使用 uv 管理。
- 不要使用 `pip install` 直接安裝專案套件。
- 新增套件時使用 `uv add`，並同步提交 `pyproject.toml` 與 `uv.lock`。
- 不要提交 `.venv/`。
- 不要提交真實 `.env`。
- 不要把 Cookie、資料庫密碼、API key、token 或 session 資訊寫死在程式碼中。

## 環境變數

請以 `.env.example` 作為範本建立本機 `.env`。範本只包含 placeholder，不包含任何真實機密。
