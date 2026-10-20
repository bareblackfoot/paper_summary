from flask import Flask, render_template, jsonify, request, send_from_directory
import json
from datetime import datetime
import os
import glob
from datetime import timedelta
import pytz
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_current_week_url():
    """Get the current week URL for Hugging Face papers"""
    # Set timezone to Seoul
    seoul_tz = pytz.timezone("Asia/Seoul")
    now = datetime.now(seoul_tz)

    # Calculate week number manually to start from Sunday
    # Get the first day of the year
    first_day = datetime(now.year, 1, 1, tzinfo=seoul_tz)
    # Adjust first day to previous Sunday if it's not already Sunday
    first_day = first_day - timedelta(days=first_day.weekday() + 1)

    # Calculate week number
    week = ((now - first_day).days // 7) + 1
    year = now.year

    # ISO week format: YYYY-WXX
    week_str = f"{year}-W{week:02d}"
    url = f"https://huggingface.co/papers/week/{week_str}"
    return url, week_str


def week_to_date_range(week_str):
    """Convert week string (e.g., '2025-W25') to date range"""
    try:
        year, week_num = week_str.split("-W")
        year = int(year)
        week_num = int(week_num)

        # Get the first day of the year
        first_day = datetime(year, 1, 1)

        # Adjust to previous Sunday if first day is not Sunday
        days_since_sunday = first_day.weekday() + 1
        first_sunday = first_day - timedelta(days=days_since_sunday)

        # Calculate the start of the target week
        week_start = first_sunday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Format dates
        start_str = week_start.strftime("%m월 %d일")
        end_str = week_end.strftime("%m월 %d일")

        return f"{start_str} ~ {end_str}"
    except:
        return week_str


def extract_papers_from_html(html_content):
    """Extract papers data from HTML content"""
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the script tag that contains the papers data
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and "const papers =" in script.string:
                # Extract the papers JSON from the script
                script_content = script.string
                start_idx = script_content.find("const papers = ") + len(
                    "const papers = "
                )
                end_idx = script_content.find(";", start_idx)
                papers_json = script_content[start_idx:end_idx]

                # Parse the JSON
                papers = json.loads(papers_json)
                return papers
    except Exception as e:
        print(f"Error extracting papers from HTML: {e}")

    return []


def load_papers(week=None):
    """Load papers from static/week directory"""
    if week:
        # 특정 주차의 논문 로드
        weekly_file = f"static/week/{week}/index.html"
        if os.path.exists(weekly_file):
            try:
                with open(weekly_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                    papers = extract_papers_from_html(html_content)
                    if papers:
                        return papers
            except Exception as e:
                print(f"Error loading papers from {weekly_file}: {e}")

        # Fallback to static/papers.json if HTML parsing fails
        if os.path.exists("static/papers.json"):
            with open("static/papers.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    else:
        # 최신 논문 로드 (static/papers.json)
        if os.path.exists("static/papers.json"):
            with open("static/papers.json", "r", encoding="utf-8") as f:
                return json.load(f)
    return []


def get_available_weeks():
    """Get list of available weeks from static/week directory"""
    weeks = []

    # static/week 폴더의 모든 주차 폴더 찾기
    if os.path.exists("static/week"):
        for item in os.listdir("static/week"):
            week_dir = os.path.join("static/week", item)
            if os.path.isdir(week_dir) and item.startswith("2025-W"):
                # 폴더명에서 주차 추출 (2025-W25 -> 2025-W25)
                week = item
                weeks.append(week)

    # 주차별로 정렬 (최신순)
    weeks.sort(reverse=True)
    return weeks


@app.route("/")
def index():
    papers = load_papers()
    available_weeks = get_available_weeks()

    # 현재 주차 계산
    _, current_week_str = get_current_week_url()
    week_range = week_to_date_range(current_week_str)

    return render_template(
        "index.html",
        papers=papers,
        available_weeks=available_weeks,
        current_week="latest",
        week_range=week_range,
        current_week_str=current_week_str,
    )


@app.route("/week/<week>")
def week_view(week):
    papers = load_papers(week)
    available_weeks = get_available_weeks()

    # 요청된 주차가 존재하지 않는 경우 404 에러
    if not papers:
        return "요청하신 주차의 논문을 찾을 수 없습니다.", 404

    week_range = week_to_date_range(week)
    return render_template(
        "index.html",
        papers=papers,
        available_weeks=available_weeks,
        current_week=week,
        week_range=week_range,
    )


@app.route("/api/papers")
def get_papers():
    week = request.args.get("week")
    papers = load_papers(week)
    return jsonify(papers)


@app.route("/api/weeks")
def get_weeks():
    """Get list of available weeks"""
    weeks = get_available_weeks()
    return jsonify(weeks)


@app.route("/static/week/<path:filename>")
def serve_static(filename):
    return send_from_directory("static/week", filename)


if __name__ == "__main__":
    app.run(debug=True)
