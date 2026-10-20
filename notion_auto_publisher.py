"""Publish the daily arXiv Top-30 report to the Notion '논문 목록' database.

각 Top 논문을 데이터베이스 항목으로 upsert한다 (URL 기준 중복 방지).
페이지 본문에는 TL;DR과 정밀 리뷰 5개 섹션이 들어간다.
"""

import json
import os
import time

from dotenv import load_dotenv
from notion_client import Client

import config

load_dotenv()

# 데이터베이스에 없으면 추가할 속성들 (기존 Name/Authors/Published/URL/Likes는 유지)
EXTRA_PROPERTIES = {
    "Score": {"number": {}},
    "Rank": {"number": {}},
    "Field": {"rich_text": {}},
    "Venue": {"rich_text": {}},
    "Date": {"rich_text": {}},
}


def _rt(text, limit=1900):
    text = (text or "").strip()
    return [{"text": {"content": text[:limit]}}]


def _paragraphs(text, limit=1900):
    """Split long text into paragraph blocks under Notion's rich_text limit."""
    text = (text or "").strip()
    blocks = []
    while text:
        chunk, text = text[:limit], text[limit:]
        blocks.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": chunk}}]},
            }
        )
    return blocks


def _heading(text):
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": _rt(text)},
    }


def _venue_text(entry):
    import venue_detect

    v = entry.get("venue_info") or {}
    return venue_detect.label(v)


def _link_paragraph(label, url):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"text": {"content": f"{label}: {url}", "link": {"url": url}}}]},
    }


def _build_blocks(entry):
    d = entry.get("deep") or {}
    blocks = []
    summary = d.get("headline") or d.get("tldr")
    if summary:
        blocks.append(
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": _rt(summary),
                    "icon": {"type": "emoji", "emoji": "💡"},
                },
            }
        )
    meta_line = (
        f"점수 {d.get('score', entry['screen_score'])}/100 · "
        f"분야 {d.get('field', '-')} · robotics relevance {entry['robotics_relevance']}/10"
    )
    venue = _venue_text(entry)
    if venue:
        meta_line += f" · 학회 {venue}"
    blocks.extend(_paragraphs(meta_line))

    if d.get("headline"):
        sections = [
            ("무슨 문제인가", d.get("problem")),
            ("어떻게 푸나", d.get("method")),
            ("결과", d.get("results")),
            ("한계", d.get("limits")),
            ("누리랩 연구와의 연결", d.get("lab_relevance")),
        ]
    else:  # 2026-10-12 이전 스키마
        sections = [
            ("Core Innovation & Methodology", d.get("core_innovation")),
            ("Novelty vs. Prior Works", d.get("novelty_analysis")),
            ("Benchmark Results", d.get("benchmark_results")),
            ("누리랩 연구와의 연결", d.get("recommendation")),
        ]
    for title, body in sections:
        if body:
            blocks.append(_heading(title))
            blocks.extend(_paragraphs(body))

    blocks.append(_link_paragraph("arXiv", entry["abs_url"]))
    blocks.append(_link_paragraph("alphaXiv", entry.get("alphaxiv_url") or f"https://www.alphaxiv.org/abs/{entry['arxiv_id']}"))
    for key, label in (("project", "프로젝트 페이지"), ("code", "코드"), ("video", "영상")):
        url = (d.get("links") or {}).get(key)
        if url:
            blocks.append(_link_paragraph(label, url))
    return blocks


def _ensure_properties(notion, database_id):
    """Add score/rank/field columns to the database if missing."""
    try:
        db = notion.databases.retrieve(database_id=database_id)
        missing = {k: v for k, v in EXTRA_PROPERTIES.items() if k not in db["properties"]}
        if missing:
            notion.databases.update(database_id=database_id, properties=missing)
            print(f"[notion] added properties: {list(missing)}")
        return db["properties"] | missing
    except Exception as e:
        print(f"[notion] property check failed: {e}")
        return {}


def publish_daily(date_str=None):
    token = os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get("NOTION_DATABASE_ID")
    if not token or not database_id:
        print("[notion] NOTION_TOKEN / NOTION_DATABASE_ID not set — skipping")
        return

    if date_str is None:
        dates = sorted(
            fn[:-5]
            for fn in os.listdir(config.DAILY_DIR)
            if fn.endswith(".json") and not fn.startswith(".")
        )
        if not dates:
            print("[notion] no daily reports found")
            return
        date_str = dates[-1]

    with open(os.path.join(config.DAILY_DIR, f"{date_str}.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    notion = Client(auth=token)
    props_available = _ensure_properties(notion, database_id)

    failures = 0
    for entry in data["top"]:
        d = entry.get("deep") or {}
        properties = {
            "Name": {"title": _rt(entry["title"], 1900)},
            "URL": {"url": entry["abs_url"]},
            "Authors": {"rich_text": _rt(", ".join(entry["authors"]))},
            "Published": {"rich_text": _rt(date_str)},
        }
        if "Score" in props_available:
            properties["Score"] = {"number": d.get("score", entry["screen_score"])}
        if "Rank" in props_available:
            properties["Rank"] = {"number": entry["rank"]}
        if "Field" in props_available:
            properties["Field"] = {"rich_text": _rt(d.get("field", ""))}
        if "Venue" in props_available:
            properties["Venue"] = {"rich_text": _rt(_venue_text(entry))}
        if "Date" in props_available:
            properties["Date"] = {"rich_text": _rt(date_str)}

        try:
            existing = notion.databases.query(
                database_id=database_id,
                filter={"property": "URL", "url": {"equals": entry["abs_url"]}},
            )
            if existing["results"]:
                page_id = existing["results"][0]["id"]
                notion.pages.update(page_id=page_id, properties=properties)
                print(f"[notion] updated: #{entry['rank']} {entry['title'][:50]}")
            else:
                page = notion.pages.create(
                    parent={"database_id": database_id}, properties=properties
                )
                notion.blocks.children.append(
                    block_id=page["id"], children=_build_blocks(entry)
                )
                print(f"[notion] created: #{entry['rank']} {entry['title'][:50]}")
        except Exception as e:
            failures += 1
            print(f"[notion] failed for {entry['arxiv_id']}: {e}")
        time.sleep(0.4)  # Notion rate limit (3 req/s)

    print(f"[notion] published {len(data['top']) - failures}/{len(data['top'])} papers for {date_str}")
    return failures


# 하위 호환용 별칭 (구 파이프라인이 부르던 이름)
def create_notion_page():
    publish_daily()


if __name__ == "__main__":
    import sys

    # deploy.yml keeps this step continue-on-error so the site still deploys, but a
    # non-zero exit marks the step failed in the run log instead of hiding it
    # (it silently failed every day from 2026-08-20 to 2026-10-13).
    sys.exit(1 if publish_daily() else 0)
