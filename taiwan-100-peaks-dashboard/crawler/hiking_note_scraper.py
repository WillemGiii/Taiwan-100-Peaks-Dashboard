"""
健行筆記軌跡數據爬蟲模組
=============================

本模組示範如何透過 ``requests`` 發送 AJAX 請求，並以 ``BeautifulSoup``
解析「健行筆記」(hiking.biji.co) 軌跡相關 GPX 紀錄頁面，
擷取各項運動指標（里程、耗時、爬升高度、下降高度、紀錄日期等）。

使用方式::

    python hiking_note_scraper.py
"""

import os
import re
import pprint
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# 常數設定
# ---------------------------------------------------------------------------

BASE_URL: str = "https://hiking.biji.co/trail/ajax/load_related_gpx"
REQUEST_TIMEOUT_SECONDS: int = 30
REQUEST_MAX_RETRIES: int = 3
REQUEST_RETRY_BACKOFF_SECONDS: int = 2

# 目標山岳與其在健行筆記對應的軌跡 ID
TRAIL_DATA: dict[str, int] = {
    "tao_mountain": 429,
    "tao_kalaye": 1746,
    "chiyou_pintian": 1737,
    "mt_beidawu": 1750,
    "mt_taguan": 1761,
    "mt_hijiayang": 531,
    "mt_junda": 500,
    "mt_xue_east": 1734,
    "mt_guanshangling": 1760,
    "hehuan_north": 288,
    "hehuan_north_west": 536,
    "mt_jade_front": 68,
}

# Cookies are read from HIKING_NOTE_COOKIE to avoid committing session data.
# Copy the browser Cookie header into the environment variable when needed.
def parse_cookie_header(cookie_header: str) -> dict[str, str]:
    cookies: dict[str, str] = {}
    for item in cookie_header.split(";"):
        if "=" not in item:
            continue
        name, value = item.split("=", 1)
        name = name.strip()
        if name:
            cookies[name] = value.strip()
    return cookies


COOKIES: dict[str, str] = parse_cookie_header(os.getenv("HIKING_NOTE_COOKIE", ""))

HEADERS: dict[str, str] = {
    "accept": "*/*",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
    "referer": "https://hiking.biji.co/index.php?q=trail&act=detail&id=288",
    "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/149.0.0.0 Safari/537.36"
    ),
}


# ---------------------------------------------------------------------------
# 工具函式
# ---------------------------------------------------------------------------


def parse_duration_to_minutes(duration_text: str) -> int:
    """將「X 小時 Y 分鐘」格式的字串轉換為總分鐘數。

    Args:
        duration_text: 原始耗時文字，例如 ``"2 小時 30 分鐘"`` 或 ``"45 分鐘"``。

    Returns:
        換算後的總分鐘數（整數）。若無法解析則回傳 ``0``。
    """
    hour_match = re.search(r"(\d+)\s*小時", duration_text)
    minute_match = re.search(r"(\d+)\s*分鐘", duration_text)

    hours: int = int(hour_match.group(1)) if hour_match else 0
    minutes: int = int(minute_match.group(1)) if minute_match else 0

    return hours * 60 + minutes


def parse_record(
    record_tag: "BeautifulSoup",
    trail_name: str,
) -> Optional[dict[str, object]]:
    """從單筆 ``<li>`` 標籤解析出軌跡紀錄資料。

    Args:
        record_tag: 代表一筆軌跡紀錄的 BeautifulSoup Tag 物件（``<li>``）。
        trail_name: 對應的山岳/路線名稱（英文識別碼）。

    Returns:
        包含以下欄位的字典：

        - ``trail_name`` (str): 路線識別碼
        - ``distance_km`` (str): 里程（公里）
        - ``duration_minutes`` (int): 耗時（分鐘）
        - ``ascent_m`` (str): 爬升高度（公尺）
        - ``descent_m`` (str): 下降高度（公尺）
        - ``record_date`` (str): 紀錄日期

        若解析失敗則回傳 ``None``。
    """
    # 里程（km）
    distance_text: str = record_tag.select("span")[0].text
    distance_match = re.search(r"([\d.]+)", distance_text)
    if not distance_match:
        return None
    distance_km: str = distance_match.group(1)

    # 耗時（分鐘）
    duration_text: str = record_tag.select("span.truncate")[0].text.strip()
    duration_minutes: int = parse_duration_to_minutes(duration_text)

    # 爬升高度（m）：移除千位分隔符後再解析
    ascent_text: str = record_tag.select("span")[2].text.replace(",", "").strip()
    ascent_match = re.search(r"(\d+)", ascent_text)
    if not ascent_match:
        return None
    ascent_m: str = ascent_match.group(1)

    # 下降高度（m）：移除千位分隔符後再解析
    descent_text: str = record_tag.select("span")[3].text.replace(",", "").strip()
    descent_match = re.search(r"(\d+)", descent_text)
    if not descent_match:
        return None
    descent_m: str = descent_match.group(1)

    # 紀錄日期
    record_date: str = record_tag.select("span")[4].text.strip()

    return {
        "trail_name": trail_name,
        "distance_km": distance_km,
        "duration_minutes": duration_minutes,
        "ascent_m": ascent_m,
        "descent_m": descent_m,
        "record_date": record_date,
    }


def fetch_page_records(
    hiking_note_id: int,
    page: int,
    trail_name: str,
) -> list[dict[str, object]] | None:
    """向健行筆記 AJAX 端點請求指定頁碼的軌跡紀錄，並解析回傳。

    Args:
        hiking_note_id: 健行筆記山岳/路線頁面的數字 ID。
        page: 欲抓取的分頁編號（從 1 開始）。
        trail_name: 對應的山岳/路線名稱（英文識別碼），用於標記資料來源。

    Returns:
        該頁所有有效紀錄的字典清單；若該頁無資料則回傳空清單。
        若該頁請求重試後仍失敗，回傳 ``None`` 讓呼叫端略過單頁。
    """
    params: dict[str, object] = {
        "id": hiking_note_id,
        "page": page,
        "device": "computer",
    }

    response: requests.Response | None = None
    for attempt in range(1, REQUEST_MAX_RETRIES + 1):
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                cookies=COOKIES,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as exc:
            print(
                f"  第 {page} 頁請求失敗 "
                f"({attempt}/{REQUEST_MAX_RETRIES}): {exc}"
            )
            if attempt < REQUEST_MAX_RETRIES:
                wait_seconds = REQUEST_RETRY_BACKOFF_SECONDS * attempt
                print(f"    {wait_seconds} 秒後重試。")
                time.sleep(wait_seconds)
            else:
                print(f"  第 {page} 頁重試後仍失敗，略過此頁。")
                return None

    if response is None:
        return None

    try:
        raw_html: str = response.json()["data"]["list"]
    except (KeyError, TypeError, ValueError) as exc:
        print(f"  第 {page} 頁回應格式無法解析，略過此頁: {exc}")
        return None

    # 健行筆記回傳的是 <li> 片段，需包在 <ul> 中才能正確解析
    soup = BeautifulSoup(f"<ul>{raw_html}</ul>", "lxml")
    li_tags = soup.ul.find_all("li", class_="flex", recursive=False)

    records: list[dict[str, object]] = []
    for li in li_tags:
        record = parse_record(li, trail_name)
        if record is not None:
            records.append(record)

    return records


def scrape_all_trails(
    trail_data: dict[str, int],
    max_pages: int = 9,
) -> list[dict[str, object]]:
    """爬取 ``trail_data`` 中所有路線的多頁軌跡紀錄。

    Args:
        trail_data: 路線識別碼（鍵）與健行筆記 ID（值）的對應字典。
        max_pages: 每條路線最多抓取的頁數（預設 9 頁）。

    Returns:
        所有路線、所有分頁的軌跡紀錄合併清單。
    """
    all_records: list[dict[str, object]] = []

    for trail_name, hiking_note_id in trail_data.items():
        print(f"\n{'=' * 50}")
        print(f"路線: {trail_name}（ID: {hiking_note_id}）")
        print("=" * 50)

        for page in range(1, max_pages + 1):
            page_records = fetch_page_records(hiking_note_id, page, trail_name)

            if page_records is None:
                continue

            # 若該頁無資料，代表已到最後一頁，提前結束
            if not page_records:
                print(f"  第 {page} 頁無資料，停止翻頁。")
                break

            print(f"  第 {page} 頁：取得 {len(page_records)} 筆紀錄")
            pprint.pprint(page_records)
            all_records.extend(page_records)

    return all_records


# ---------------------------------------------------------------------------
# 主程式入口
# ---------------------------------------------------------------------------


def main() -> None:
    """主執行函式：爬取健行筆記各路線軌跡資料並印出結果。"""
    all_records = scrape_all_trails(TRAIL_DATA, max_pages=9)

    print(f"\n{'=' * 50}")
    print(f"總計取得 {len(all_records)} 筆軌跡紀錄")
    print("=" * 50)


if __name__ == "__main__":
    main()
