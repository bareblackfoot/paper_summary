"""Static site generator for the daily arXiv Top-30 reports.

Reads database/daily/{date}.md (+ .json metadata) and renders:
  static/index.html               – latest daily report
  static/daily/{date}/index.html  – archive page per day
  static/daily/{date}/report.md   – raw markdown
  static/daily/{date}/data.json   – raw evaluation data
"""

import json
import os
import shutil
import sys

import markdown
from jinja2 import Environment, FileSystemLoader

import config

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MD_EXTENSIONS = ["extra", "md_in_html", "sane_lists", "toc"]


def available_dates():
    if not os.path.isdir(config.DAILY_DIR):
        return []
    dates = [
        fn[:-3]
        for fn in os.listdir(config.DAILY_DIR)
        if fn.endswith(".md") and len(fn) == 13  # YYYY-MM-DD.md
    ]
    dates.sort(reverse=True)
    return dates


def render_report(md_text):
    return markdown.markdown(md_text, extensions=MD_EXTENSIONS)


def load_meta(date):
    path = os.path.join(config.DAILY_DIR, f"{date}.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def attach_figures(date, top):
    """Mark which Top-K papers have a stored figure.

    Checked at render time rather than read from the report JSON, so a day whose
    figures have aged out of static/figures simply renders without them.
    """
    fig_dir = os.path.join("static", "figures", date)
    for paper in top:
        name = f"{paper.get('arxiv_id', '')}.webp"
        paper["figure"] = name if os.path.exists(os.path.join(fig_dir, name)) else ""
    return top


def generate_static_html():
    dates = available_dates()
    if not dates:
        print("No daily reports found in", config.DAILY_DIR)
        return

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("daily.html")
    os.makedirs("static", exist_ok=True)

    for i, date in enumerate(dates):
        meta = load_meta(date)
        top = attach_figures(date, meta.get("top", []))
        synthesis_html = ""
        if meta.get("synthesis_md"):
            synthesis_html = render_report(meta["synthesis_md"])

        prev_date = dates[i + 1] if i + 1 < len(dates) else None
        next_date = dates[i - 1] if i > 0 else None

        contexts = [("daily", f"static/daily/{date}", "../../")]
        if i == 0:
            contexts.append(("root", "static", ""))

        for kind, out_dir, prefix in contexts:
            os.makedirs(out_dir, exist_ok=True)
            html = template.render(
                date=date,
                weekday=meta.get("weekday", ""),
                dates=dates,
                prev_date=prev_date,
                next_date=next_date,
                prefix=prefix,
                meta=meta,
                top=top,
                screened=meta.get("screened", []),
                synthesis_html=synthesis_html,
            )
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)

        # raw files for download / programmatic use
        day_dir = f"static/daily/{date}"
        md_path = os.path.join(config.DAILY_DIR, f"{date}.md")
        if os.path.exists(md_path):
            shutil.copy2(md_path, os.path.join(day_dir, "report.md"))
        json_path = os.path.join(config.DAILY_DIR, f"{date}.json")
        if os.path.exists(json_path):
            shutil.copy2(json_path, os.path.join(day_dir, "data.json"))

        print(f"Generated static/daily/{date}/index.html")

    # copy shared assets (logo etc.)
    if os.path.isdir("templates/assets"):
        os.makedirs("static/assets", exist_ok=True)
        for fn in os.listdir("templates/assets"):
            shutil.copy2(os.path.join("templates/assets", fn), os.path.join("static/assets", fn))
        print("Copied templates/assets to static/assets")

    print(f"Generated static/index.html (latest: {dates[0]})")


if __name__ == "__main__":
    generate_static_html()
    print("Static site generated in static directory")
