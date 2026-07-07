# PROJECT_CONTEXT.md

# 臺灣百岳單攻互動式地圖網站

## 0. 文件用途

本文件提供給 Codex 或其他 AI Coding Agent 作為專案上下文資訊文件使用。

Codex 在協助開發本專案時，應優先閱讀並遵守本文件內容，包含：

- 專案目標
- 技術堆疊
- 目前完成進度
- 尚未完成事項
- API 規格
- 專案目錄結構
- Docker 與 Git 開發規範
- 不應任意修改的開發規則

除非使用者明確要求，Codex 不應主動更換技術棧，也不應擴充超出 MVP 範圍的功能。

---

## 1. 專案一句話說明

本專案是一個以 Leaflet 呈現臺灣百岳單攻路線資料的互動式地圖網站，使用者點擊山岳後，可查看該山的登山統計儀表板。

---

## 2. 專案目標

本專案目標是建立一個臺灣百岳單攻資料視覺化網站，讓使用者可以透過地圖快速查看山岳位置與基本登山資訊。

MVP 階段重點是：

1. 使用 Leaflet 顯示臺灣地圖。
2. 在地圖上標示至少 5 座百岳。
3. 使用者點擊 Marker 後，可以查看山名與海拔。
4. 後續可串接後端 API、PostgreSQL 與 HikingNote 爬蟲資料。
5. 最終點擊山岳後，可顯示登山統計儀表板。

---

## 3. 技術堆疊

### 3.1 前端

使用技術：

- HTML
- CSS
- JavaScript
- Leaflet.js
- Chart.js

用途：

- `Leaflet.js`：呈現臺灣地圖與山岳 Marker。
- `Chart.js`：呈現山岳統計儀表板圖表，例如平均耗時、平均距離與月份分布。

---

### 3.2 後端

使用技術：

- Python
- FastAPI

用途：

- 提供 RESTful API。
- 回傳山岳基本資料。
- 回傳指定山岳的統計資料。
- 與 PostgreSQL 資料庫連線。

---

### 3.3 資料庫

使用技術：

- PostgreSQL

用途：

- 儲存山岳基本資料。
- 儲存 HikingNote 公開登山紀錄。
- 提供 API 查詢與統計資料來源。

---

### 3.4 資料處理與爬蟲

使用技術：

- Python
- Requests
- BeautifulSoup
- Pandas

用途：

- 蒐集 HikingNote 公開登山紀錄。
- 整理登山日期、登山距離、登山總耗時等欄位。
- 進行資料清洗與聚合。
- 將清洗後資料寫入 PostgreSQL。

MVP 階段爬蟲可先採手動執行，不一定要加入自動排程。

---

### 3.5 容器化環境

使用技術：

- Docker
- Docker Compose

用途：

- 建立獨立的容器式開發環境。
- 降低不同開發者的環境安裝差異。
- 確保前端、後端、資料庫與資料處理流程可以穩定重現。

建議使用 Docker Compose 管理以下服務：

| Service | 說明 |
| --- | --- |
| `frontend` | 前端地圖與儀表板介面 |
| `backend` | FastAPI API 服務 |
| `db` | PostgreSQL 資料庫 |
| `crawler` | 登山紀錄爬蟲與資料清洗程式 |

MVP 階段 Docker 至少需完成：

1. 可以使用 Docker Compose 一次啟動前端、後端與資料庫。
2. 後端服務可以成功連線 PostgreSQL。
3. 前端可以透過 API 取得資料並顯示在地圖上。
4. 爬蟲程式可以在容器中執行，並將資料寫入資料庫。

---

## 4. 版本控制規範

本專案使用 Git 進行版本控制，確保每個功能完成後都能留下可追蹤的開發紀錄。

### 4.1 開發原則

1. 每完成一個小功能即建立一次 commit。
2. Commit 訊息需清楚描述本次完成內容。
3. 重要階段需建立 Git tag。
4. 若使用 AI 工具協助開發，每次要求 AI 修改程式前，需先確認目前版本已 commit。
5. 若 AI 修改後造成錯誤，可透過 Git 回復到上一個穩定版本。

---

### 4.2 建議 Git Tag

```text
v0.1-map-prototype
v0.2-database-api
v0.3-crawler-import
v0.4-dashboard
v1.0-mvp
```

---

### 4.3 建議開發分支

```text
main                穩定版本
develop             整合開發版本
feature/map         地圖功能
feature/api         後端 API
feature/crawler     爬蟲功能
feature/dashboard   儀表板功能
feature/docker      容器化環境
```

---

## 5. 專案目錄結構

目前建議專案目錄如下：

```text
project-root/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── backend/
│   ├── main.py
│   ├── routers/
│   └── services/
├── crawler/
│   └── hikingnote_crawler.py
├── database/
│   └── schema.sql
├── docker-compose.yml
└── README.md
```

---

## 6. 目前完成進度

### 6.1 已完成

目前已完成以下項目：

1. Leaflet 地圖可正常顯示臺灣地圖。
2. 已手動建立 5 座山岳資料。
3. Marker 可以顯示在地圖上。
4. 點擊 Marker 可顯示山名與海拔。

---

### 6.2 尚未完成

目前尚未完成以下項目：

1. 後端 API。
2. PostgreSQL 串接。
3. HikingNote 爬蟲。
4. 山岳儀表板。
5. Chart.js 圖表整合。
6. Docker Compose 完整服務串接。

---

## 7. API 規格

以下為預計實作的 API 規格。

---

### 7.1 `GET /api/mountains`

用途：取得所有山岳基本資料。

#### Response 範例

```json
[
  {
    "id": 1,
    "name": "玉山主峰",
    "latitude": 23.470002,
    "longitude": 120.957274,
    "elevation": 3952
  }
]
```

#### 欄位說明

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| `id` | number | 山岳 ID |
| `name` | string | 山岳名稱 |
| `latitude` | number | 緯度 |
| `longitude` | number | 經度 |
| `elevation` | number | 海拔高度，單位為公尺 |

---

### 7.2 `GET /api/mountains/{id}/stats`

用途：取得指定山岳的統計資料。

#### Request Path Parameter

| 參數 | 型別 | 說明 |
| --- | --- | --- |
| `id` | number | 山岳 ID |

#### Response 範例

```json
{
  "mountain_id": 1,
  "average_duration_minutes": 720,
  "average_distance_km": 21.5,
  "monthly_distribution": {
    "1": 5,
    "2": 8,
    "3": 10
  }
}
```

#### 欄位說明

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| `mountain_id` | number | 山岳 ID |
| `average_duration_minutes` | number | 平均登山耗時，單位為分鐘 |
| `average_distance_km` | number | 平均登山距離，單位為公里 |
| `monthly_distribution` | object | 各月份登山紀錄數量 |

---

### 7.3 資料不足時的回傳建議

若指定山岳沒有足夠資料，API 不應讓前端出現錯誤，建議回傳如下格式：

```json
{
  "mountain_id": 1,
  "average_duration_minutes": null,
  "average_distance_km": null,
  "monthly_distribution": {},
  "data_status": "insufficient_data",
  "message": "目前此山岳資料不足，暫時無法產生統計資訊。"
}
```

前端收到 `data_status = "insufficient_data"` 時，應顯示提示文字，而不是渲染空白圖表或讓程式報錯。

---

## 8. 資料庫設計方向

資料庫 schema 應放在：

```text
database/schema.sql
```

若 Codex 修改資料表結構，必須同步更新 `database/schema.sql`。

---

### 8.1 建議資料表：`mountains`

用途：儲存山岳基本資料。

建議欄位：

```sql
CREATE TABLE mountains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    elevation INTEGER NOT NULL
);
```

---

### 8.2 建議資料表：`hike_records`

用途：儲存 HikingNote 公開登山紀錄。

建議欄位：

```sql
CREATE TABLE hike_records (
    id SERIAL PRIMARY KEY,
    mountain_id INTEGER REFERENCES mountains(id),
    hike_date DATE,
    duration_minutes INTEGER,
    distance_km NUMERIC(6, 2),
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 9. 儀表板統計邏輯

### 9.1 平均耗時

指定山岳的平均登山耗時：

```text
average_duration_minutes = SUM(duration_minutes) / record_count
```

注意：

- 單位為分鐘。
- 若 `record_count = 0`，不可除以 0。
- 若資料不足，需回傳資料不足狀態。

---

### 9.2 平均距離

指定山岳的平均登山距離：

```text
average_distance_km = SUM(distance_km) / record_count
```

注意：

- 單位為公里。
- 若資料不足，需回傳 `null` 或資料不足狀態。

---

### 9.3 月份分布

根據 `hike_date` 取出月份，統計每個月份的紀錄數量。

範例：

```json
{
  "1": 5,
  "2": 8,
  "3": 10
}
```

後續若要給 Chart.js 使用，可以再調整為陣列格式。

---

## 10. 下一步建議開發順序

### Phase 1：整理前端靜態地圖

目前前端已有基礎功能，下一步建議先穩定現有功能。

工作項目：

1. 確認 `frontend/index.html` 可正常載入。
2. 確認 `frontend/style.css` 負責樣式。
3. 確認 `frontend/app.js` 負責 Leaflet 初始化、Marker 建立與點擊事件。
4. 確認 5 座山岳資料格式一致。
5. 不要在此階段加入後端 API。

建議 commit：

```text
feat: add leaflet map prototype
```

建議 tag：

```text
v0.1-map-prototype
```

---

### Phase 2：建立 FastAPI 後端

工作項目：

1. 建立 `backend/main.py`。
2. 建立基本 FastAPI app。
3. 建立 `GET /api/mountains`。
4. 先使用假資料回傳，確認前端可以 fetch API。
5. 確認 CORS 設定。

建議 commit：

```text
feat: add mountains api endpoint
```

---

### Phase 3：建立 PostgreSQL 與 schema

工作項目：

1. 建立 `database/schema.sql`。
2. 建立 `mountains` 資料表。
3. 建立 `hike_records` 資料表。
4. 加入 5 座山岳 seed data。
5. 確認 FastAPI 可以連線 PostgreSQL。

建議 commit：

```text
feat: add postgres schema and seed data
```

建議 tag：

```text
v0.2-database-api
```

---

### Phase 4：前端改接 API

工作項目：

1. 將前端靜態山岳資料改成呼叫 `GET /api/mountains`。
2. 用 API 回傳資料產生 Marker。
3. 保留 Marker 點擊顯示山名與海拔功能。
4. 若 API 失敗，前端應顯示錯誤提示。

建議 commit：

```text
feat: connect frontend map to mountains api
```

---

### Phase 5：建立統計 API

工作項目：

1. 建立 `GET /api/mountains/{id}/stats`。
2. 從 `hike_records` 聚合資料。
3. 回傳平均耗時。
4. 回傳平均距離。
5. 回傳月份分布。
6. 處理資料不足情境。

建議 commit：

```text
feat: add mountain stats api
```

---

### Phase 6：建立山岳儀表板

工作項目：

1. Marker 點擊後呼叫 `GET /api/mountains/{id}/stats`。
2. 顯示平均耗時。
3. 顯示平均距離。
4. 使用 Chart.js 顯示月份分布。
5. 若資料不足，顯示提示文字。

建議 commit：

```text
feat: add mountain dashboard
```

建議 tag：

```text
v0.4-dashboard
```

---

### Phase 7：建立 HikingNote 爬蟲

工作項目：

1. 建立 `crawler/hikingnote_crawler.py`。
2. 使用 Requests 與 BeautifulSoup 取得公開登山紀錄。
3. 清洗登山日期。
4. 清洗登山距離。
5. 清洗登山總耗時並轉為分鐘。
6. 寫入 PostgreSQL。
7. MVP 階段先採手動執行，不需自動排程。

注意：

- 不要高頻率請求網站。
- 需尊重網站使用規範。
- 若頁面格式不一致，需保留可追蹤的錯誤訊息。

建議 commit：

```text
feat: add hikingnote crawler import script
```

建議 tag：

```text
v0.3-crawler-import
```

---

### Phase 8：Docker Compose 整合

工作項目：

1. 建立 `docker-compose.yml`。
2. 建立 frontend service。
3. 建立 backend service。
4. 建立 db service。
5. 建立 crawler service。
6. 確認使用 Docker Compose 可以啟動完整開發環境。
7. 確認 backend 可以連線 db。
8. 確認 frontend 可以呼叫 backend。

建議 commit：

```text
chore: add docker compose development environment
```

---

## 11. 開發規則

Codex 開發時必須遵守以下規則：

1. 不要任意更換技術棧。
2. 不要修改已經能正常運作的功能，除非任務明確要求。
3. 每次只完成一個小功能。
4. 新增功能後需說明修改了哪些檔案。
5. 若修改資料表，必須同步更新 `database/schema.sql`。
6. 所有功能完成後需建議 Git commit 訊息。
7. 不要把資料庫密碼、API key 或機密資訊寫死在程式碼中。
8. 優先使用 `.env` 或 Docker Compose environment variables 管理環境變數。
9. 修改 API response 格式時，必須同步檢查前端使用資料的地方。
10. 不要主動新增登入、會員、收藏、天氣、GPX、手機 App 等非 MVP 功能。

---

## 12. Codex 每次任務執行前檢查

Codex 在修改程式前，應先檢查：

1. 目前任務目標是什麼？
2. 本次是否只修改一個小功能？
3. 是否會影響已完成的 Leaflet 地圖功能？
4. 是否需要修改 `schema.sql`？
5. 是否需要更新 README？
6. 是否需要補充 API response 範例？
7. 修改完成後應建議哪一個 commit message？

---

## 13. MVP 驗收標準

MVP 完成時，至少需符合以下條件：

1. 使用者可以打開網站並看到臺灣地圖。
2. 地圖上至少有 5 座山岳 Marker。
3. Marker 可以被點擊。
4. 點擊後可以顯示山名與海拔。
5. 前端可以透過 API 取得山岳資料。
6. PostgreSQL 可以儲存山岳與登山紀錄。
7. 後端可以計算指定山岳的平均耗時。
8. 後端可以計算指定山岳的平均距離。
9. 後端可以計算指定山岳的一到十二月登山紀錄分布。
10. 前端可以顯示山岳統計儀表板。
11. 資料不足時，畫面需顯示提示文字，而不是程式錯誤。

---

## 14. 暫不納入 MVP 的功能

以下功能暫不納入 MVP。除非使用者明確要求，Codex 不應主動實作：

1. 使用者登入與會員系統。
2. 使用者收藏山岳。
3. 路線導航。
4. 即時定位。
5. GPX 軌跡播放。
6. 天氣預報串接。
7. 離線地圖。
8. 手機 App。
9. 後台管理系統。
10. 自動排程爬蟲。
11. 完整百岳資料庫。
12. 難度評分模型。

---

## 15. 建議 README 內容

`README.md` 後續至少應包含：

1. 專案簡介。
2. 技術堆疊。
3. 專案目錄結構。
4. Docker Compose 啟動方式。
5. 前端啟動方式。
6. 後端啟動方式。
7. PostgreSQL 設定方式。
8. 爬蟲手動執行方式。
9. API 規格。
10. Git commit 與 tag 建議。

---

## 16. 最重要的開發方向

本專案第一版不是完整登山平台，而是一個小型 MVP。

目前最重要的方向是：

1. 保持 Leaflet 地圖穩定。
2. 逐步接上 FastAPI。
3. 再接 PostgreSQL。
4. 再做統計 API。
5. 最後整合 Chart.js 儀表板。
6. 爬蟲可以放在後段，且 MVP 階段可先手動執行。

請優先保持功能清楚、資料流穩定、程式容易回復，不要一次做太多功能。
