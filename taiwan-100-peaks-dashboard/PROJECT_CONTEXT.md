# Project Context

## 專案目標

本專案是臺灣百岳單攻資料視覺化地圖，MVP 目標是讓使用者透過地圖查看可單攻百岳，並於後續串接 FastAPI、PostgreSQL 與 HikingNote 登山紀錄統計資料。

## 本次初始化狀態

- 專案根目錄為 `taiwan-100-peaks-dashboard/`。
- backend 與 crawler 各自使用獨立 uv project。
- 既有 crawler 已放在 `crawler/hiking_note_scraper.py`。
- backend、frontend、db 目前只建立 placeholder，不實作正式 API、Leaflet 地圖或 PostgreSQL schema。

## 開發規則

- 不要主動擴充 MVP 以外功能。
- 不要新增登入、會員、收藏、天氣、GPX、手機 App、自動排程等功能。
- 不要重寫 `crawler/hiking_note_scraper.py` 的核心爬蟲邏輯，除非使用者明確要求。
- 不要把 Cookie、密碼、API key、token 或 session 寫入程式碼。
- Python dependencies 必須使用 uv 管理，不使用 `pip install`。
- 不要提交 `.venv/`、`.env` 或任何真實機密。

## 技術方向

- Frontend: HTML, CSS, JavaScript, Leaflet.js, Chart.js。
- Backend: Python, FastAPI。
- Database: PostgreSQL。
- Crawler: Python, Requests, BeautifulSoup。

