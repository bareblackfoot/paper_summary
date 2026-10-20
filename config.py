import os

from dotenv import load_dotenv

load_dotenv()

# --- arXiv collection ---
# 매일 확인할 arXiv 신규 목록 (New submissions만 집계, cross-list/replacement 제외)
ARXIV_CATEGORIES = ["cs.CV", "cs.LG", "cs.RO", "cs.CL", "cs.AI"]
ARXIV_LIST_URL = "https://arxiv.org/list/{cat}/new?skip=0&show=2000"
ARXIV_REQUEST_DELAY = 3.0  # arXiv rate-limit etiquette (1 req / 3 sec)
USER_AGENT = "paper-summary-daily/2.0 (+https://github.com/bareblackfoot/paper_summary)"

# --- OpenAI models ---
# 1차 스크리닝(전체 신규 논문 초록 채점)은 저렴한 모델,
# Top 30 정밀 리뷰(PDF 원문 검토)는 고성능 모델을 사용한다.
# 계정에서 해당 모델을 쓸 수 없으면 fallback 목록에서 순서대로 대체된다.
SCREEN_MODEL = os.getenv("OPENAI_SCREEN_MODEL", "gpt-5-nano")
DEEP_MODEL = os.getenv("OPENAI_DEEP_MODEL", "gpt-5-mini")
SCREEN_MODEL_FALLBACKS = ["gpt-5-nano", "gpt-5-mini", "gpt-4.1-mini", "gpt-4o-mini"]
DEEP_MODEL_FALLBACKS = ["gpt-5-mini", "gpt-5", "gpt-4.1", "gpt-4o"]

# --- lab profile ---
# 평가 프롬프트에 들어가는 연구실 정보. LAB_PROFILE에 대표 논문·프로젝트·키워드를
# 채우면 relevance 평가와 "연구 연결점" 항목이 더 정확해진다.
LAB_NAME = "누리랩 (NuRI Lab)"
LAB_PROFILE = ""  # 예: "대표 연구: ... / 진행 중 프로젝트: ... / 주요 장비: ..."

# --- pipeline ---
TOP_K = 15  # PDF 원문까지 정밀 리뷰할 논문 수
SCREEN_BATCH_SIZE = 10  # 1차 스크리닝 시 한 번의 LLM 호출로 채점할 논문 수
SCREEN_WORKERS = 4  # 1차 스크리닝 동시 호출 수
DEEP_WORKERS = 3  # 정밀 리뷰 동시 호출 수

# PDF 원문 텍스트가 너무 길면 앞부분(method/experiments)과
# 뒷부분(limitations/appendix)을 남기고 중간을 자른다.
PDF_HEAD_CHARS = 50000
PDF_TAIL_CHARS = 15000

# --- paths ---
DAILY_DIR = "database/daily"
SEEN_IDS_PATH = "database/seen_ids.json"
SEEN_IDS_KEEP_DAYS = 60

# Top-K 대표 그림은 static/figures/<날짜>/ 에 쌓이므로 같은 창으로 정리한다.
FIGURE_KEEP_DAYS = 60
