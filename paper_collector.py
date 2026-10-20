"""Daily arXiv paper evaluation pipeline.

1. cs.CV / cs.LG / cs.RO / cs.CL / cs.AI 의 arXiv "new" 목록에서
   New submissions만 전수 수집 (cross-list, replacement 제외, 중복 병합)
2. 모든 신규 논문을 LLM으로 1차 스크리닝 (100점 만점 + robotics relevance)
3. 상위 30편은 arXiv PDF 원문을 내려받아 정밀 리뷰 (10개 항목)
4. 트렌드 종합 / 연구 방향 제안 / 필독 논문 섹션 합성
5. database/daily/{date}.json 과 {date}.md 리포트 저장
"""

import argparse
import html as html_lib
import io
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

import pytz
import requests

import config
from arxiv_source import collect_new_submissions

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WEEKDAY_KR = ["월", "화", "수", "목", "금", "토", "일"]

_print_lock = threading.Lock()


def log(msg):
    with _print_lock:
        print(msg, flush=True)


# ---------------------------------------------------------------------------
# Evaluation criteria (shared by screening and deep review)
# ---------------------------------------------------------------------------

EVAL_CRITERIA = """[평가 기준 — 종합 점수 100점 만점]
1) 기존 방식 대비 novelty와 conceptual leap
2) 해당 학계에 미칠 potential impact
3) technical / empirical conviction (방법의 타당성, 실험적 증거의 강도)
4) CVPR/ICCV/ECCV/NeurIPS/ICML/ICLR/AAAI/ACL/EMNLP/NAACL/CoRL/RSS/ICRA/IROS 같은
   top-tier conference에서 oral/highlight로 선정될 만한 수준인지
5) robot learning, embodied AI 및 아래 우선 주제와의 relevance (중요한 평가 요소)

[우선적으로 높게 평가할 주제]
- VLA(vision-language-action) 및 generalist robot policy
- manipulation / dexterous manipulation
- world models
- test-time optimization / inference-time planning
- failure detection · diagnosis · recovery
- counterfactual / causal reasoning
- robot memory
- language feedback 기반 learning
- RL / IL (reinforcement / imitation learning)
- skill chaining, long-horizon planning, TAMP
- active perception / next-best-view
- object-centric 3D/4D representation, 3D Gaussian Splatting
- scene graph / semantic mapping
- tactile perception
- navigation / VLN, embodied spatial reasoning
- video understanding, multimodal foundation models, representation learning,
  generative models, efficient inference 등도 robotics 문제에 새로운 원리나
  방법론을 제공하는 경우 높게 평가

[감점 요소]
- 단순 benchmark 점수 개선
- 기존 architecture에 작은 module을 추가한 수준의 incremental engineering
- 단순 scale-up, 특정 dataset에 대한 fine-tuning 위주의 기여

[가점 요소]
- 새로운 문제 설정(problem formulation), 새로운 representation,
  새로운 learning/inference paradigm, 일반화 가능한 이론·도구, 강한 실험적 증거

[주의]
- 논문에 학회 accept/oral/highlight 정보가 이미 적혀 있어도 점수가 그 사실에
  자동으로 끌려가지 않도록 독립적으로 평가할 것."""

# 연구실 프로필이 설정되어 있으면 평가 기준에 포함 (config.LAB_PROFILE 참조)
if config.LAB_PROFILE.strip():
    EVAL_CRITERIA += (
        f"\n\n[연구실 프로필 — {config.LAB_NAME}]\n{config.LAB_PROFILE.strip()}"
    )

SCREEN_SYSTEM = (
    "너는 robot learning / computer vision 연구실의 PI를 보조하는 senior reviewer다. "
    "arXiv 신규 논문을 제목/초록 기반으로 일관된 기준으로 채점한다. "
    "반드시 유효한 JSON만 출력한다.\n\n" + EVAL_CRITERIA
)

SCREEN_SCHEMA = (
    '{"evaluations": [{"id": "<arxiv_id>", "score": <0-100 정수>, '
    '"robotics_relevance": <0-10 정수, robot learning/embodied AI 및 우선 주제와의 관련도>, '
    '"field": "<분야 태그 (예: VLA, Manipulation, World Model, Embodied AI, 3D Vision, '
    'Navigation, RL, Video, Multimodal, CV, NLP, LG)>", '
    '"reason": "<한 줄 평가 근거, 한국어>"}]}'
)

DEEP_SYSTEM = (
    "너는 top-tier 학회(CVPR/NeurIPS/CoRL/ICLR 등)의 area chair 수준 reviewer이자, "
    "robot learning / computer vision 연구실 PI의 논문 스크리닝을 돕는 조수다. "
    "제공된 논문 원문은 PDF에서 자동 추출한 텍스트라 수식/표가 깨져 있을 수 있다. "
    "수치는 반드시 제공된 텍스트에서 확인된 것만 쓰고, 확인할 수 없는 수치는 추측하지 말고 "
    "'본문에서 확인 불가'라고 표시하라. 저자의 주장(claim)과 실제 실험 결과를 구분해서 서술하라. "
    "반드시 유효한 JSON만 출력한다.\n\n" + EVAL_CRITERIA
)

DEEP_SCHEMA = """{
  "score": <0-100 정수, 종합 평가 점수>,
  "field": "<분야 (예: VLA, Manipulation, World Model, Embodied AI, 3D Vision, Navigation, RL, Video, Multimodal, CV, NLP, LG)>",
  "tldr": "<2문장 요약: 무엇을 어떻게 해서 무엇이 좋아졌는지, 쉬운 한국어로>",
  "core_innovation": "<핵심 아이디어·문제 설정·방법(architecture/representation/objective/inference). '- '로 시작하는 불릿 3~4개, 각 1~2문장>",
  "novelty_analysis": "<가장 가까운 prior works/baselines 대비 본질적 차이. 불릿 2~3개. 단순 feature 추가인지 paradigm/problem formulation이 새로운지 구분하고, novelty가 제한적이면 명시>",
  "benchmark_results": "<핵심 benchmark·metric·수치, strongest baseline 대비 개선폭, generalization/real-robot 결과, 중요 ablation. 불릿 3~5개, 숫자 중심. 저자 주장과 실험 결과를 구분하고 확인 불가한 수치는 '본문에서 확인 불가'>",
  "venue_score": <0-100 정수, top-tier conference 적합성 점수>,
  "venue": "<가장 적합한 venue (예: CoRL, CVPR, NeurIPS, ICLR, RSS, ICRA ...)>",
  "venue_justification": "<2~3문장: oral/highlight 가능성 등 강점 + 약점/rejection risk 1문장>",
  "recommendation": "<누리랩(NuRI Lab)의 연구 주제(VLA, failure detection/recovery, test-time optimization, world model, counterfactual reasoning, robot memory, manipulation, active perception, object-centric 3DGS, scene graph)와의 연결점과 활용 아이디어. 불릿 2~3개>"
}"""

SYNTH_SYSTEM = (
    "너는 robot learning / computer vision 연구실의 PI를 돕는 research strategist다. "
    "요청된 마크다운 섹션만 출력하고 다른 말은 하지 않는다."
)


# ---------------------------------------------------------------------------
# OpenAI helpers
# ---------------------------------------------------------------------------


def get_client():
    from openai import OpenAI

    return OpenAI()


def resolve_model(client, requested, fallbacks):
    """Return the first model the account can actually use."""
    candidates = [requested] + [m for m in fallbacks if m != requested]
    for m in candidates:
        try:
            client.models.retrieve(m)
            return m
        except Exception:
            continue
    return requested


def call_llm_json(client, model, system, user, max_retries=3):
    """Call the chat API and parse a JSON object from the response."""
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
            )
            content = resp.choices[0].message.content or ""
            content = content.strip()
            if content.startswith("```"):
                content = content.strip("`")
                if content.startswith("json"):
                    content = content[4:]
            return json.loads(content)
        except Exception as e:
            last_err = e
            wait = 5 * (attempt + 1)
            log(f"[llm] error (attempt {attempt + 1}/{max_retries}): {e} — retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_err}")


def call_llm_text(client, model, system, user, max_retries=3):
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            last_err = e
            wait = 5 * (attempt + 1)
            log(f"[llm] error (attempt {attempt + 1}/{max_retries}): {e} — retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_err}")


# ---------------------------------------------------------------------------
# Stage 1 — screening (all new papers, title+abstract)
# ---------------------------------------------------------------------------


def build_screen_user(batch):
    lines = [
        "다음 arXiv 신규 논문들을 위 평가 기준에 따라 채점하라.",
        "아래 JSON 스키마로만 답하라 (모든 논문 포함, id는 그대로 복사):",
        SCREEN_SCHEMA,
        "",
    ]
    for i, p in enumerate(batch, 1):
        lines.append(f"[{i}] id: {p['arxiv_id']}")
        lines.append(f"제목: {p['title']}")
        lines.append(f"Subjects: {p['subjects']}")
        if p.get("comments"):
            lines.append(f"Comments: {p['comments'][:300]}")
        lines.append(f"초록: {p['abstract'][:2600]}")
        lines.append("")
    return "\n".join(lines)


def _apply_screen_result(paper, ev):
    try:
        paper["screen_score"] = max(0, min(100, int(ev.get("score", 0))))
    except (TypeError, ValueError):
        paper["screen_score"] = 0
    try:
        paper["robotics_relevance"] = max(0, min(10, int(ev.get("robotics_relevance", 0))))
    except (TypeError, ValueError):
        paper["robotics_relevance"] = 0
    paper["field"] = str(ev.get("field", "") or "").strip()[:60]
    paper["screen_reason"] = str(ev.get("reason", "") or "").strip()


def screen_papers(client, model, papers, ckpt=None, date_str=None):
    """Score every paper; returns the same list with screen_* fields added."""
    ckpt = ckpt if ckpt is not None else {"screen": {}, "deep": {}, "text_source": {}}

    # Reuse checkpointed screening results from an interrupted run.
    todo = []
    for p in papers:
        saved = ckpt["screen"].get(p["arxiv_id"])
        if saved:
            _apply_screen_result(p, saved)
        else:
            todo.append(p)
    if len(todo) < len(papers):
        log(f"[screen] {len(papers) - len(todo)} papers restored from checkpoint")

    batches = [
        todo[i : i + config.SCREEN_BATCH_SIZE]
        for i in range(0, len(todo), config.SCREEN_BATCH_SIZE)
    ]
    log(f"[screen] {len(todo)} papers in {len(batches)} batches (model: {model})")

    done_count = [0]

    def _checkpoint_batch(batch):
        if date_str is None:
            return
        for p in batch:
            if "screen_score" in p:
                ckpt["screen"][p["arxiv_id"]] = {
                    "score": p["screen_score"],
                    "robotics_relevance": p["robotics_relevance"],
                    "field": p["field"],
                    "reason": p["screen_reason"],
                }
        save_checkpoint(date_str, ckpt)

    def _run_batch(batch):
        result = call_llm_json(client, model, SCREEN_SYSTEM, build_screen_user(batch))
        evals = {str(ev.get("id", "")).strip(): ev for ev in result.get("evaluations", [])}
        missing = []
        for p in batch:
            ev = evals.get(p["arxiv_id"])
            if ev:
                _apply_screen_result(p, ev)
            else:
                missing.append(p)
        # Retry papers the model skipped, individually.
        for p in missing:
            try:
                result = call_llm_json(client, model, SCREEN_SYSTEM, build_screen_user([p]))
                evs = result.get("evaluations", [])
                if evs:
                    _apply_screen_result(p, evs[0])
            except Exception as e:
                log(f"[screen] failed for {p['arxiv_id']}: {e}")
        _checkpoint_batch(batch)
        with _print_lock:
            done_count[0] += 1
        log(f"[screen] batch {done_count[0]}/{len(batches)} done")

    with ThreadPoolExecutor(max_workers=config.SCREEN_WORKERS) as ex:
        futures = [ex.submit(_run_batch, b) for b in batches]
        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                log(f"[screen] batch failed: {e}")

    for p in papers:
        p.setdefault("screen_score", 0)
        p.setdefault("robotics_relevance", 0)
        p.setdefault("field", "")
        p.setdefault("screen_reason", "(스크리닝 실패)")
    return papers


# ---------------------------------------------------------------------------
# Stage 2 — deep review of top-K (full PDF)
# ---------------------------------------------------------------------------


def sanitize_text(text):
    """PDF 추출 텍스트의 unpaired surrogate 등 인코딩 불가 문자를 제거."""
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")


def extract_pdf_text(pdf_bytes):
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(pdf_bytes))
    return sanitize_text("\n".join((page.extract_text() or "") for page in reader.pages))


def truncate_body(text):
    limit = config.PDF_HEAD_CHARS + config.PDF_TAIL_CHARS
    if len(text) <= limit:
        return text
    return (
        text[: config.PDF_HEAD_CHARS]
        + "\n\n[... 분량 제한으로 본문 중간 생략 ...]\n\n"
        + text[-config.PDF_TAIL_CHARS :]
    )


def fetch_paper_text(arxiv_id, with_pdf=False):
    """Download the paper full text. Returns (body, source_label).

    with_pdf=True returns (body, source_label, pdf_bytes) so callers can inspect
    the PDF layout (venue_detect) without a second download; pdf_bytes is None
    when the PDF could not be fetched.
    """
    headers = {"User-Agent": config.USER_AGENT}
    pdf_bytes = None

    def done(body, source):
        return (body, source, pdf_bytes) if with_pdf else (body, source)

    try:
        r = requests.get(f"https://arxiv.org/pdf/{arxiv_id}", headers=headers, timeout=180)
        r.raise_for_status()
        pdf_bytes = r.content
        text = extract_pdf_text(r.content)
        if len(text.strip()) > 2000:
            return done(truncate_body(text), "PDF 전문")
    except Exception as e:
        log(f"[deep] PDF extraction failed for {arxiv_id}: {e}")
    time.sleep(config.ARXIV_REQUEST_DELAY)
    try:
        from bs4 import BeautifulSoup

        r = requests.get(f"https://arxiv.org/html/{arxiv_id}v1", headers=headers, timeout=120)
        if r.ok:
            text = sanitize_text(
                BeautifulSoup(r.text, "html.parser").get_text("\n", strip=True)
            )
            if len(text.strip()) > 2000:
                return done(truncate_body(text), "arXiv HTML 전문")
    except Exception as e:
        log(f"[deep] HTML fallback failed for {arxiv_id}: {e}")
    import alphaxiv_source

    text = alphaxiv_source.fetch_fulltext(arxiv_id)
    if text:
        return done(truncate_body(sanitize_text(text)), "alphaXiv 추출 전문")
    return done(None, "초록만 (원문 추출 실패)")


def build_deep_user(paper, body, source_label):
    meta = (
        f"arXiv ID: {paper['arxiv_id']}\n"
        f"제목: {paper['title']}\n"
        f"저자: {', '.join(paper['authors'][:20])}\n"
        f"Subjects: {paper['subjects']}\n"
        f"Comments: {paper.get('comments') or '(없음)'}\n"
        f"1차 스크리닝: {paper['screen_score']}점 / robotics relevance {paper['robotics_relevance']}/10 "
        f"(근거: {paper['screen_reason']})\n"
        f"원문 소스: {source_label}\n"
    )
    body_text = body if body else f"(원문 추출 실패 — 아래 초록만 제공)\n\n초록: {paper['abstract']}"
    return (
        "아래 논문을 정밀 평가하여 다음 JSON 스키마로만 답하라.\n"
        "모든 텍스트 필드는 한국어로 쓰되 기술 용어는 영어를 그대로 사용하라.\n"
        "문체: 짧은 문장, 불릿('- ') 위주, 군더더기 없이 읽기 쉽게. "
        "자연스러운 서술형(예: '~한다', '~를 보였다', '~할 수 있다')으로 쓰고, "
        "명령형(예: '~하라', '~트리거하라')은 절대 쓰지 마라. "
        "단 정보 밀도는 유지 — 방법 이름, 핵심 수치, baseline 이름은 반드시 포함하라. "
        "PI가 하루 30편을 빠르게 screening하는 용도다.\n"
        "Method, related work, experiments, ablations, limitations의 핵심 내용을 "
        "제공된 텍스트에서 확인 가능한 범위에서 반영하라.\n\n"
        + DEEP_SCHEMA
        + "\n\n[논문 메타데이터]\n"
        + meta
        + "\n[논문 원문 (자동 추출)]\n"
        + body_text
    )


def deep_review_papers(client, model, top_papers, ckpt=None, date_str=None):
    """Fetch full texts (serially, politely) then review in parallel."""
    ckpt = ckpt if ckpt is not None else {"screen": {}, "deep": {}, "text_source": {}}

    # Reuse checkpointed deep reviews from an interrupted run.
    done = {}
    todo = []
    for p in top_papers:
        saved = ckpt["deep"].get(p["arxiv_id"])
        if saved:
            done[p["arxiv_id"]] = saved
            p["deep"] = saved
            p["text_source"] = ckpt["text_source"].get(p["arxiv_id"], saved.get("text_source", ""))
        else:
            todo.append(p)
    if done:
        log(f"[deep] {len(done)} reviews restored from checkpoint")

    log(f"[deep] downloading {len(todo)} papers for full-text review")
    fetched = []
    for i, p in enumerate(todo):
        if i > 0:
            time.sleep(config.ARXIV_REQUEST_DELAY)
        body, source = fetch_paper_text(p["arxiv_id"])
        log(f"[deep] {i + 1}/{len(todo)} {p['arxiv_id']}: {source}")
        fetched.append((p, body, source))

    log(f"[deep] reviewing with model: {model}")
    results = {}

    def _review(p, body, source):
        user = build_deep_user(p, body, source)
        data = call_llm_json(client, model, DEEP_SYSTEM, user)
        try:
            data["score"] = max(0, min(100, int(data.get("score", 0))))
        except (TypeError, ValueError):
            data["score"] = p["screen_score"]
        try:
            data["venue_score"] = max(0, min(100, int(data.get("venue_score", 0))))
        except (TypeError, ValueError):
            data["venue_score"] = 0
        data["text_source"] = source
        return data

    with ThreadPoolExecutor(max_workers=config.DEEP_WORKERS) as ex:
        futures = {
            ex.submit(_review, p, body, source): p["arxiv_id"] for p, body, source in fetched
        }
        for f in as_completed(futures):
            pid = futures[f]
            try:
                results[pid] = f.result()
                log(f"[deep] review done: {pid} → {results[pid]['score']}점")
                if date_str is not None:
                    ckpt["deep"][pid] = results[pid]
                    ckpt["text_source"][pid] = results[pid].get("text_source", "")
                    save_checkpoint(date_str, ckpt)
            except Exception as e:
                log(f"[deep] review FAILED for {pid}: {e}")
                results[pid] = None

    for p, body, source in fetched:
        p["deep"] = results.get(p["arxiv_id"])
        p["text_source"] = source
    return top_papers


# ---------------------------------------------------------------------------
# Stage 3 — synthesis (trends / strategy / must-read)
# ---------------------------------------------------------------------------


def build_synth_user(top_papers):
    lines = []
    for rank, p in enumerate(top_papers, 1):
        d = p.get("deep") or {}
        lines.append(
            f"{rank}. [{p['arxiv_id']}] {p['title']}\n"
            f"   분야: {d.get('field') or p['field']} / 점수: {d.get('score', p['screen_score'])} / "
            f"robotics relevance: {p['robotics_relevance']}/10\n"
            f"   핵심: {(d.get('core_innovation') or p['screen_reason'])[:600]}\n"
            f"   추천 이유: {(d.get('recommendation') or '')[:400]}"
        )
    paper_list = "\n".join(lines)
    return f"""오늘의 arXiv Top {len(top_papers)} 논문 목록이 아래에 있다.
이를 바탕으로 다음 세 개 섹션을 정확히 아래 제목의 '## ' 마크다운 헤딩으로 작성하라.
문체: 짧은 문장, 불릿 위주, 읽기 쉽게. 본문은 자연스러운 서술형('~한다', '~가 유망하다',
'~할 수 있다')으로 쓰고 명령형('~하라')은 절대 쓰지 마라.
논문 언급 시 [제목 일부](https://arxiv.org/abs/<id>) 링크 사용.

## 오늘의 핵심 연구 트렌드 종합
- 논문별 요약 반복이 아니라 여러 논문을 관통하는 기술적 흐름과 paradigm shift를 합성하라.
- **불릿 4~6개**, 각 불릿은 '**흐름 이름** — 설명 1~2문장' 형식.
- VLA, world models, test-time computation, failure detection/recovery, memory,
  multimodal/video, 3D/4D understanding, active perception, embodied reasoning 관점에서
  어떤 문제가 새로 중요해지고 있고 기존 접근의 한계가 무엇인지 담아라.

## 유망 연구 방향 및 프로젝트 제안
- 오늘 관찰된 research gap을 근거로, 누리랩(robot learning / CV 연구실)이 6~18개월 내
  수행 가능한 project topic을 **4~6개** 제안하라.
- 각 주제는 '**제목**' 뒤에 불릿 3~4개로: 핵심 research question / 접근 방법과 novelty /
  왜 지금인지·경쟁 prior works / 난이도·risk와 target venue.
- VLA + failure recovery, VLA + test-time optimization, world model + planning,
  counterfactual physical reasoning, reusable robot memory, object-centric 3D/4D,
  active manipulation/perception, tactile reasoning, scene-graph memory 방향을 우선하라.

## 오늘 반드시 읽어야 할 논문
- Top {len(top_papers)} 중 5~10편. '- [제목](https://arxiv.org/abs/<id>) — 한 줄 이유' 형식.
- 이유는 누리랩(VLA, failure recovery, test-time optimization, world model,
  counterfactual reasoning, robot memory, manipulation, active perception,
  object-centric 3DGS, scene graph)과의 연결점 중심으로.

[오늘의 Top 논문 목록]
{paper_list}"""


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------


def format_authors(authors, limit=8):
    if not authors:
        return "(저자 정보 없음)"
    if len(authors) <= limit:
        return ", ".join(authors)
    return ", ".join(authors[:limit]) + f" 외 {len(authors) - limit}명"


def venue_label(v):
    import venue_detect

    return venue_detect.label(v)


def build_report_md(
    date_str,
    weekday,
    category_counts,
    unique_count,
    evaluated_count,
    top_papers,
    all_papers,
    synthesis_md,
    screen_model,
    deep_model,
):
    total_new = sum(category_counts.values())
    cat_rows = "\n".join(f"| {cat} | {n} |" for cat, n in category_counts.items())

    parts = [
        f"# 오늘의 arXiv Top {len(top_papers)}: {date_str} ({weekday})",
        "",
        "> 대상: " + ", ".join(category_counts.keys()) + " 의 **New submissions 전수 평가**",
        "> (cross-list, replacement 제외 · 여러 목록에 중복된 논문은 1편으로 병합)",
        "",
        f"**신규 논문 수: 전체 {total_new}편 → 중복 제거 후 {unique_count}편 (이번 평가 대상 {evaluated_count}편)**",
        "",
        "| 카테고리 | New submissions |",
        "|---|---|",
        cat_rows,
        "",
        f"*1차 스크리닝: 전체 {evaluated_count}편을 제목/초록 기반으로 채점({screen_model}) → "
        f"상위 {len(top_papers)}편은 arXiv 원문을 내려받아 정밀 리뷰({deep_model}) 후 최종 점수 산정.*",
        "",
        "---",
        "",
        f"## Top {len(top_papers)}",
    ]

    for rank, p in enumerate(top_papers, 1):
        d = p.get("deep") or {}
        score = d.get("score", p["screen_score"])
        field = d.get("field") or p["field"] or "-"
        aid = p["arxiv_id"]
        links = [
            f"[arXiv](https://arxiv.org/abs/{aid})",
            f"[PDF](https://arxiv.org/pdf/{aid})",
            f"[alphaXiv](https://www.alphaxiv.org/abs/{aid})"
            + (" (요약 있음)" if p.get("alphaxiv_overview") else ""),
        ]
        for key, name in (("project", "프로젝트 페이지"), ("code", "코드"), ("video", "영상")):
            url = (d.get("links") or {}).get(key)
            if url:
                links.append(f"[{name}]({url})")
        venue = p.get("venue_info") or {}
        parts += [
            "",
            f"### {rank}. {p['title']} ({score}점)",
            "",
            " · ".join(links),
            "",
            f"- **저자**: {format_authors(p['authors'])}",
            f"- **분야**: {field} · robotics relevance {p['robotics_relevance']}/10 · 1차 스크리닝 {p['screen_score']}점",
        ]
        if venue.get("venue"):
            parts.append(f"- **학회**: {venue_label(venue)} · 근거: {venue['evidence']}")
        parts.append(f"- **읽은 원문**: {p.get('text_source', '초록만')}")
        if d.get("headline"):
            parts += [
                "",
                f"> {d['headline']}",
                "",
                "**무슨 문제인가**",
                "",
                d.get("problem", ""),
                "",
                "**어떻게 푸나**",
                "",
                d.get("method", ""),
                "",
                "**결과**",
                "",
                d.get("results", ""),
                "",
                "**한계**",
                "",
                d.get("limits", ""),
                "",
                "**누리랩 연구와의 연결**",
                "",
                d.get("lab_relevance", ""),
            ]
            if d.get("figure_caption"):
                parts += ["", f"*대표 그림: {d['figure_caption']}*"]
            if p.get("alphaxiv_video"):
                cap = d.get("video_caption", "")
                parts += ["", f"*영상: [{cap or '프로젝트 영상'}]({p['alphaxiv_video']}) (alphaXiv 요약에서 가져옴)*"]
        elif d:
            # 2026-10-12 이전 스키마 (tldr / core_innovation / ...)
            parts += ["", f"> {d.get('tldr', '')}"]
            for title, key in (
                ("Core innovation & methodology", "core_innovation"),
                ("Novelty vs. prior works", "novelty_analysis"),
                ("Benchmark results", "benchmark_results"),
                ("누리랩 연구와의 연결", "recommendation"),
            ):
                if d.get(key):
                    parts += ["", f"**{title}**", "", d[key]]
        else:
            parts += [
                "",
                f"*(정밀 리뷰 실패. 1차 스크리닝 근거: {p['screen_reason']})*",
            ]
        parts.append("")
        parts.append("---")

    if synthesis_md:
        parts += ["", synthesis_md, "", "---"]

    # Full screening table (collapsed)
    rows = []
    ranked_all = sorted(
        all_papers,
        key=lambda x: (x["screen_score"], x["robotics_relevance"]),
        reverse=True,
    )
    for i, p in enumerate(ranked_all, 1):
        title = html_lib.escape(p["title"])
        reason = html_lib.escape(p.get("screen_reason", ""))
        rows.append(
            f"<tr><td>{i}</td><td><a href='https://arxiv.org/abs/{p['arxiv_id']}'>{title}</a></td>"
            f"<td>{p['screen_score']}</td><td>{p['robotics_relevance']}</td>"
            f"<td>{html_lib.escape(p.get('field', ''))}</td><td>{reason}</td></tr>"
        )
    parts += [
        "",
        "<details>",
        f"<summary><strong>전체 1차 스크리닝 결과 ({len(ranked_all)}편, 점수순)</strong></summary>",
        "",
        "<table><thead><tr><th>#</th><th>제목</th><th>점수</th><th>Robotics</th><th>분야</th><th>한 줄 근거</th></tr></thead><tbody>",
        "\n".join(rows),
        "</tbody></table>",
        "",
        "</details>",
        "",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Checkpointing (crash/interruption 시 LLM 결과를 잃지 않도록 중간 저장)
# ---------------------------------------------------------------------------

_ckpt_lock = threading.Lock()


def checkpoint_path(date_str):
    return os.path.join(config.DAILY_DIR, f".checkpoint-{date_str}.json")


def load_checkpoint(date_str):
    path = checkpoint_path(date_str)
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            log(
                f"[ckpt] resuming from checkpoint: {len(data.get('screen', {}))} screened, "
                f"{len(data.get('deep', {}))} deep-reviewed"
            )
            return data
    except Exception as e:
        log(f"[ckpt] failed to load checkpoint: {e}")
    return {"screen": {}, "deep": {}, "text_source": {}}


def save_checkpoint(date_str, ckpt):
    with _ckpt_lock:
        os.makedirs(config.DAILY_DIR, exist_ok=True)
        tmp = checkpoint_path(date_str) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(ckpt, f, ensure_ascii=False)
        os.replace(tmp, checkpoint_path(date_str))


def clear_checkpoint(date_str):
    try:
        if os.path.exists(checkpoint_path(date_str)):
            os.remove(checkpoint_path(date_str))
        # 오래된(7일 이상) 체크포인트도 정리 — 해당 mailing은 /new에서 이미 사라져 재개 불가
        cutoff = (datetime.now(pytz.timezone("Asia/Seoul")) - timedelta(days=7)).strftime("%Y-%m-%d")
        for fn in os.listdir(config.DAILY_DIR):
            if fn.startswith(".checkpoint-") and fn.endswith(".json"):
                d = fn[len(".checkpoint-") : -len(".json")]
                if d < cutoff:
                    os.remove(os.path.join(config.DAILY_DIR, fn))
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Seen-id tracking (so weekends / repeated runs skip already-evaluated mailings)
# ---------------------------------------------------------------------------


def load_seen_ids():
    try:
        if os.path.exists(config.SEEN_IDS_PATH):
            with open(config.SEEN_IDS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        log(f"[seen] failed to load seen ids: {e}")
    return {}


def save_seen_ids(seen, new_ids, date_str):
    for pid in new_ids:
        seen[pid] = date_str
    cutoff = (datetime.now(pytz.timezone("Asia/Seoul")) - timedelta(days=config.SEEN_IDS_KEEP_DAYS)).strftime(
        "%Y-%m-%d"
    )
    seen = {pid: d for pid, d in seen.items() if d >= cutoff}
    os.makedirs(os.path.dirname(config.SEEN_IDS_PATH), exist_ok=True)
    with open(config.SEEN_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Daily arXiv paper evaluation pipeline")
    parser.add_argument("--top-k", type=int, default=config.TOP_K, help="정밀 리뷰할 논문 수")
    parser.add_argument("--max-papers", type=int, default=None, help="(디버그) 스크리닝할 논문 수 제한")
    parser.add_argument("--collect-only", action="store_true", help="수집/파싱만 하고 LLM 호출 안 함")
    parser.add_argument("--dry-run", action="store_true", help="결과 파일과 seen_ids를 저장하지 않음")
    parser.add_argument("--force", action="store_true", help="이미 평가한 논문도 다시 평가")
    parser.add_argument("--no-synthesis", action="store_true", help="트렌드/전략 섹션 생성 생략")
    parser.add_argument(
        "--backfill",
        metavar="YYYY-MM-DD",
        default=None,
        help="지난 mailing(최근 5회 이내)을 /recent 페이지에서 재구성해 평가",
    )
    args = parser.parse_args()

    seoul_now = datetime.now(pytz.timezone("Asia/Seoul"))
    log(f"=== arXiv daily pipeline started at {seoul_now.isoformat()} ===")

    # Stage 0 — collect
    if args.backfill:
        from arxiv_source import collect_from_recent

        target = datetime.strptime(args.backfill, "%Y-%m-%d").date()
        papers, category_counts, mailing_date = collect_from_recent(target)
    else:
        papers, category_counts, mailing_date = collect_new_submissions()
    unique_count = len(papers)
    if not papers:
        log("No new submissions found (arXiv holiday/weekend?). Exiting.")
        return

    date_str = (mailing_date or seoul_now.date()).strftime("%Y-%m-%d")
    weekday = WEEKDAY_KR[(mailing_date or seoul_now.date()).weekday()]

    seen = load_seen_ids()
    if not args.force:
        fresh = [p for p in papers if p["arxiv_id"] not in seen]
    else:
        fresh = papers
    if not fresh:
        log(f"All {unique_count} papers were already evaluated (mailing {date_str}). Exiting.")
        return
    if len(fresh) < unique_count:
        log(f"[seen] skipping {unique_count - len(fresh)} already-evaluated papers")

    if args.max_papers:
        fresh = fresh[: args.max_papers]
    log(f"Evaluating {len(fresh)} papers for mailing {date_str} ({weekday})")

    if args.collect_only:
        for p in fresh[:10]:
            log(f"- {p['arxiv_id']} [{p['primary_subject']}] {p['title'][:90]}")
        log("--collect-only: stopping before LLM stages.")
        return

    client = get_client()
    screen_model = resolve_model(client, config.SCREEN_MODEL, config.SCREEN_MODEL_FALLBACKS)
    deep_model = resolve_model(client, config.DEEP_MODEL, config.DEEP_MODEL_FALLBACKS)
    log(f"Models — screening: {screen_model}, deep review: {deep_model}")

    # Checkpoint: 중단된 실행이 있으면 LLM 결과를 재사용
    ckpt_date = None if args.dry_run else date_str
    ckpt = load_checkpoint(date_str) if ckpt_date else {"screen": {}, "deep": {}, "text_source": {}}

    # Stage 1 — screening
    screen_papers(client, screen_model, fresh, ckpt=ckpt, date_str=ckpt_date)

    # Stage 2 — deep review of top-K
    ranked = sorted(
        fresh, key=lambda p: (p["screen_score"], p["robotics_relevance"]), reverse=True
    )
    top = ranked[: args.top_k]
    deep_review_papers(client, deep_model, top, ckpt=ckpt, date_str=ckpt_date)

    # Final ranking: deep score first, tie-break by venue score then robotics relevance
    def final_key(p):
        d = p.get("deep") or {}
        return (
            d.get("score", p["screen_score"]),
            d.get("venue_score", 0),
            p["robotics_relevance"],
        )

    top.sort(key=final_key, reverse=True)

    # Stage 3 — synthesis
    synthesis_md = ""
    if not args.no_synthesis:
        log("[synth] generating trends / strategy / must-read sections")
        try:
            synthesis_md = call_llm_text(
                client, deep_model, SYNTH_SYSTEM, build_synth_user(top)
            )
        except Exception as e:
            log(f"[synth] failed: {e}")

    # Assemble & save
    report_md = build_report_md(
        date_str,
        weekday,
        category_counts,
        unique_count,
        len(fresh),
        top,
        fresh,
        synthesis_md,
        screen_model,
        deep_model,
    )

    payload = {
        "date": date_str,
        "weekday": weekday,
        "generated_at": seoul_now.isoformat(),
        "categories": list(category_counts.keys()),
        "category_counts": category_counts,
        "total_new": sum(category_counts.values()),
        "total_unique": unique_count,
        "evaluated": len(fresh),
        "screen_model": screen_model,
        "deep_model": deep_model,
        "top": [
            {
                "rank": i + 1,
                "arxiv_id": p["arxiv_id"],
                "title": p["title"],
                "authors": p["authors"],
                "subjects": p["subjects"],
                "primary_subject": p["primary_subject"],
                "listed_in": p.get("listed_in", []),
                "comments": p.get("comments", ""),
                "abs_url": p["abs_url"],
                "pdf_url": p["pdf_url"],
                "screen_score": p["screen_score"],
                "robotics_relevance": p["robotics_relevance"],
                "text_source": p.get("text_source", ""),
                "deep": p.get("deep"),
            }
            for i, p in enumerate(top)
        ],
        "screened": [
            {
                "arxiv_id": p["arxiv_id"],
                "title": p["title"],
                "primary_subject": p["primary_subject"],
                "listed_in": p.get("listed_in", []),
                "screen_score": p["screen_score"],
                "robotics_relevance": p["robotics_relevance"],
                "field": p.get("field", ""),
                "reason": p.get("screen_reason", ""),
            }
            for p in sorted(
                fresh,
                key=lambda x: (x["screen_score"], x["robotics_relevance"]),
                reverse=True,
            )
        ],
        "synthesis_md": synthesis_md,
    }

    if args.dry_run:
        log("--dry-run: skipping file writes. Report preview (first 3000 chars):")
        log(report_md[:3000])
        return

    os.makedirs(config.DAILY_DIR, exist_ok=True)
    json_path = os.path.join(config.DAILY_DIR, f"{date_str}.json")
    md_path = os.path.join(config.DAILY_DIR, f"{date_str}.md")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    log(f"Saved {json_path} and {md_path}")

    # Notion 게시 (NOTION_TOKEN 미설정 시 자동 스킵)
    try:
        from notion_auto_publisher import publish_daily

        publish_daily(date_str)
    except Exception as e:
        log(f"[notion] publish failed (skipping): {e}")

    save_seen_ids(seen, [p["arxiv_id"] for p in fresh], date_str)
    clear_checkpoint(date_str)
    log("Done!")


if __name__ == "__main__":
    main()
