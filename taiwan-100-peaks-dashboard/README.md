# Taiwan 100 Peaks One-Day Hike Dashboard

臺灣百岳單攻資料視覺化 MVP。前端使用 Leaflet 顯示臺灣地圖與山岳 Marker，點擊 Marker 後會透過 FastAPI 查詢 PostgreSQL 中的 HikingNote 登山紀錄統計，並用 Chart.js 顯示平均耗時、平均距離與一到十二月紀錄分布。

## 專案結構

```text
taiwan-100-peaks-dashboard/
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── app.js
│       ├── map.js
│       └── dashboard.js
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── scripts/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
├── crawler/
├── db/
│   ├── init.sql
│   └── seed.sql
├── docker-compose.yml
├── .env.example
└── README.md
```

## 一鍵啟動

先建立本機 `.env`：

```powershell
Copy-Item .env.example .env
```

啟動全部服務：

```powershell
docker compose up --build
```

停止服務：

```powershell
docker compose down
```

清除 PostgreSQL volume：

```powershell
docker compose down -v
```

## 服務網址

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- Swagger/OpenAPI: http://localhost:8000/docs

## API 範例

```text
GET http://localhost:8000/api/mountains
GET http://localhost:8000/api/mountains/288/dashboard
```

`/api/mountains` 會回傳 PostgreSQL `mountains` 資料表中的山岳路線資料。`/api/mountains/{mountain_id}/dashboard` 會用 `hiking_records` 即時計算平均耗時、平均距離與月份分布，不 hard-code 統計結果。

## Docker 資料庫初始化

Backend container 啟動時會先執行：

```text
uv run alembic upgrade head
uv run python scripts/seed_database.py
```

這會建立 `mountains` / `hiking_records` 資料表，並匯入 `db/seed.sql`。Seed data 會放入山岳資料與一筆 `hehuan_north` 測試登山紀錄，讓地圖 Marker 與合歡北峰 dashboard 可立即驗證。

## 本機開發

Backend 使用 uv：

```powershell
cd backend
uv sync
$env:DATABASE_URL="postgresql+psycopg://taiwan_peaks:change_me_for_local_dev@localhost:5432/taiwan_100_peaks"
uv run alembic upgrade head
uv run python scripts/seed_database.py
uv run uvicorn app.main:app --reload
```

Frontend 是靜態檔案，可用任一靜態 server：

```powershell
cd frontend
python -m http.server 8080
```

瀏覽器開啟 http://localhost:8080。前端預設呼叫 `http://localhost:8000`；如需調整，可在載入 `js/app.js` 前設定 `window.API_BASE_URL`。

## 環境變數

`.env.example` 提供本機開發 placeholder：

```env
POSTGRES_USER=taiwan_peaks
POSTGRES_PASSWORD=change_me_for_local_dev
POSTGRES_DB=taiwan_100_peaks
DATABASE_URL=postgresql+psycopg://taiwan_peaks:change_me_for_local_dev@localhost:5432/taiwan_100_peaks
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
HIKING_NOTE_COOKIE=name=value; another_name=another_value
```

請勿提交真實 `.env`、資料庫密碼、Cookie、API key、token 或 session。

## Crawler

既有爬蟲位於：

```text
crawler/hiking_note_scraper.py
```

不要重寫核心爬蟲邏輯，除非任務明確要求。若爬蟲需要 Cookie，請透過 `HIKING_NOTE_COOKIE` 環境變數提供。

## Python 套件管理規則

- Python dependencies 一律使用 uv 管理。
- 不要使用全域 `pip install`。
- 新增套件時使用 `uv add`，並同步提交 `pyproject.toml` 與 `uv.lock`。
- 不要提交 `.venv/`。

