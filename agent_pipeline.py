"""Claude 에이전트용 파이프라인 CLI.

LLM 평가(스크리닝·정밀 리뷰·종합)를 Claude Code 에이전트가 직접 수행할 수 있도록
파이프라인을 세 단계로 쪼갠 버전. OPENAI_API_KEY 없이 동작한다.

  python agent_pipeline.py prepare    # arXiv 수집 → work 디렉토리에 배치 파일 생성
  python agent_pipeline.py select     # 스크리닝 결과 병합 → Top-K 선정 + PDF 텍스트·그림·학회 판정·alphaXiv 요약
  python agent_pipeline.py alphaxiv   # (정밀 리뷰 직전) 아직 없는 alphaXiv 요약을 다시 받아 봄
  python agent_pipeline.py check      # 정밀 리뷰·종합의 스키마와 금지어·문체 검사 (0건이 될 때까지)
  python agent_pipeline.py assemble   # 정밀 리뷰/종합 병합 → 리포트·사이트 생성

에이전트 지침은 .claude/skills/daily-papers/SKILL.md 참조.
"""

import argparse
import glob
import json
import os
import shutil
import sys
import time
from datetime import datetime

import pytz

import requests

import alphaxiv_source
import config
import figure_extractor
import paper_collector as pc
import style_check
import venue_detect
from arxiv_source import collect_new_submissions

# 정밀 리뷰 JSON에 있어야 하는 칸 (criteria.md 정밀 리뷰 스키마와 같게 유지)
DEEP_TEXT_FIELDS = ["headline", "problem", "method", "results", "limits", "lab_relevance", "figure_caption"]
# alphaXiv 요약에 영상이 있을 때만 필요한 칸
DEEP_VIDEO_FIELD = "video_caption"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORK_ROOT = os.path.join(config.DAILY_DIR, "work")


def work_dir(date_str):
    return os.path.join(WORK_ROOT, date_str)


def _load_work(date_str=None):
    """Load the work papers.json (latest work dir if date not given)."""
    if date_str is None:
        dirs = sorted(glob.glob(os.path.join(WORK_ROOT, "*"))) if os.path.isdir(WORK_ROOT) else []
        if not dirs:
            print("ERROR: work 디렉토리가 없습니다. 먼저 prepare를 실행하세요.")
            sys.exit(1)
        date_str = os.path.basename(dirs[-1])
    path = os.path.join(work_dir(date_str), "papers.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), date_str


def _save_work(meta, date_str):
    with open(os.path.join(work_dir(date_str), "papers.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


def cmd_prepare(args):
    # alphaXiv는 클라우드 샌드박스 허용 목록에 따로 넣어야 한다. 막혀 있어도 파이프라인은
    # 계속 돌지만, 보고에 남도록 여기서 한 줄 찍는다.
    if alphaxiv_source.reachable():
        print("NET alphaxiv.org: OK")
    else:
        print("ALPHAXIV_BLOCKED: alphaxiv.org 접속 안 됨. alphaXiv 요약 없이 진행하고 최종 보고에 적을 것")
    papers, counts, mailing = collect_new_submissions()
    seoul_now = datetime.now(pytz.timezone("Asia/Seoul"))
    ref_date = mailing or seoul_now.date()
    date_str = ref_date.strftime("%Y-%m-%d")
    weekday = pc.WEEKDAY_KR[ref_date.weekday()]

    seen = pc.load_seen_ids()
    fresh = papers if args.force else [p for p in papers if p["arxiv_id"] not in seen]
    if not fresh:
        print(f"NO_NEW_PAPERS: mailing {date_str}의 {len(papers)}편은 이미 평가되었습니다. 여기서 중단하세요.")
        return
    if args.max_papers:
        fresh = fresh[: args.max_papers]

    wd = work_dir(date_str)
    for sub in ("screen_batches", "screen_results", "deep", "texts", "alphaxiv", "figs"):
        os.makedirs(os.path.join(wd, sub), exist_ok=True)

    meta = {
        "date": date_str,
        "weekday": weekday,
        "categories": list(counts.keys()),
        "category_counts": counts,
        "total_new": sum(counts.values()),
        "total_unique": len(papers),
        "evaluated": len(fresh),
        "papers": fresh,
    }
    _save_work(meta, date_str)

    batch_size = args.batch_size
    n_batches = 0
    for i in range(0, len(fresh), batch_size):
        batch = [
            {
                "arxiv_id": p["arxiv_id"],
                "title": p["title"],
                "subjects": p["subjects"],
                "comments": (p.get("comments") or "")[:300],
                "abstract": p["abstract"][:2600],
            }
            for p in fresh[i : i + batch_size]
        ]
        n_batches += 1
        with open(
            os.path.join(wd, "screen_batches", f"batch_{n_batches:03d}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(batch, f, ensure_ascii=False, indent=1)

    print(f"PREPARED: {date_str} ({weekday})")
    print(f"WORK_DIR: {wd}")
    print(f"신규 논문: 전체 {sum(counts.values())}편 / 중복 제거 {len(papers)}편 / 평가 대상 {len(fresh)}편")
    print(f"카테고리별: {counts}")
    print(f"스크리닝 배치: {n_batches}개 ({wd}/screen_batches/batch_*.json)")
    print(f"→ 각 배치를 평가해 {wd}/screen_results/ 에 같은 파일명으로 저장한 뒤 'select'를 실행하세요.")


def cmd_select(args):
    meta, date_str = _load_work(args.date)
    wd = work_dir(date_str)
    papers = meta["papers"]

    # merge screening results
    results = {}
    for path in sorted(glob.glob(os.path.join(wd, "screen_results", "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
            if isinstance(items, dict):
                items = items.get("evaluations", [])
            for ev in items:
                results[str(ev.get("id") or ev.get("arxiv_id", "")).strip()] = ev
        except Exception as e:
            print(f"WARNING: {path} 파싱 실패: {e}")

    missing = []
    for p in papers:
        ev = results.get(p["arxiv_id"])
        if ev:
            pc._apply_screen_result(p, ev)
        else:
            missing.append(p["arxiv_id"])
            p.setdefault("screen_score", 0)
            p.setdefault("robotics_relevance", 0)
            p.setdefault("field", "")
            p.setdefault("screen_reason", "(스크리닝 누락)")
    if missing:
        print(f"WARNING: {len(missing)}편의 스크리닝 결과가 없습니다: {missing[:10]}{' ...' if len(missing) > 10 else ''}")
        if not args.allow_missing:
            print("→ 누락 배치를 채운 뒤 다시 실행하거나, --allow-missing으로 무시하세요.")
            sys.exit(1)

    ranked = sorted(papers, key=lambda p: (p["screen_score"], p["robotics_relevance"]), reverse=True)
    top = ranked[: args.top_k]
    meta["top_ids"] = [p["arxiv_id"] for p in top]
    _save_work(meta, date_str)

    for sub in ("alphaxiv", "figs"):
        os.makedirs(os.path.join(wd, sub), exist_ok=True)

    print(f"TOP {len(top)} 선정 (점수순):")
    skip_existing = 0
    for i, p in enumerate(top, 1):
        aid = p["arxiv_id"]
        txt_path = os.path.join(wd, "texts", f"{aid}.txt")
        pdf_bytes = None
        if os.path.exists(txt_path) and os.path.getsize(txt_path) > 2000:
            skip_existing += 1
        else:
            if i > 1 or skip_existing == 0:
                time.sleep(config.ARXIV_REQUEST_DELAY)
            body, source, pdf_bytes = pc.fetch_paper_text(aid, with_pdf=True)
            p["text_source"] = source
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(body or f"(원문 추출 실패)\n\n초록: {p['abstract']}")

        # 학회: comments 명시 → PDF 문구 → LaTeX 양식 순 (venue_detect.py)
        if not p.get("venue_info"):
            if pdf_bytes is None:
                try:
                    time.sleep(config.ARXIV_REQUEST_DELAY)
                    r = requests.get(f"https://arxiv.org/pdf/{aid}", headers={"User-Agent": config.USER_AGENT}, timeout=180)
                    pdf_bytes = r.content if r.ok else None
                except Exception:
                    pdf_bytes = None
            p["venue_info"] = venue_detect.detect(p.get("comments"), pdf_bytes)

        fig_source = figure_extractor.fetch_figure(aid, date_str)
        p["figure_source"] = fig_source or ""
        _figure_png_for_review(date_str, aid, wd)

        ov = alphaxiv_source.fetch_overview(aid)
        p["alphaxiv_overview"] = ov["kind"] if ov else ""
        p["alphaxiv_video"] = alphaxiv_source.first_video(ov)[0]
        if ov:
            alphaxiv_source.write_overview_file(os.path.join(wd, "alphaxiv", f"{aid}.md"), aid, ov)

        print(f"  {i:2d}. [{p['screen_score']}점/R{p['robotics_relevance']}] {p['title'][:80]}")
        print(f"      → {txt_path}")
        print(f"      그림: {fig_source or '없음'} · 학회: {venue_detect.label(p['venue_info']) or '판정 못 함'}"
              f" · alphaXiv 요약: {'있음' if ov else '없음'}")
    _save_work(meta, date_str)
    n_ov = sum(1 for p in top if p.get("alphaxiv_overview"))
    print(f"alphaXiv 요약 {n_ov}/{len(top)}편 ({wd}/alphaxiv/). 정밀 리뷰 직전에 'alphaxiv'를 한 번 더 돌려 새로 생긴 것을 받으세요.")
    print(f"→ 각 논문 텍스트를 읽고 정밀 리뷰 JSON을 {wd}/deep/<arxiv_id>.json 으로 저장한 뒤,")
    print(f"  트렌드 종합을 {wd}/synthesis.md 로 저장하고 'check' → 'assemble'을 실행하세요.")


def _figure_png_for_review(date_str, arxiv_id, wd):
    """PNG copy of the card figure in the work dir, so the reviewing agent can look at it."""
    src = figure_extractor.figure_path(date_str, arxiv_id)
    if not os.path.exists(src):
        return
    try:
        from PIL import Image

        Image.open(src).convert("RGB").save(os.path.join(wd, "figs", f"{arxiv_id}.png"))
    except Exception as e:
        print(f"      (리뷰용 PNG 변환 실패: {e})")


def cmd_alphaxiv(args):
    """Fetch alphaXiv overviews that did not exist at select time."""
    meta, date_str = _load_work(args.date)
    wd = work_dir(date_str)
    os.makedirs(os.path.join(wd, "alphaxiv"), exist_ok=True)
    by_id = {p["arxiv_id"]: p for p in meta["papers"]}
    new = 0
    for aid in meta.get("top_ids", []):
        p = by_id[aid]
        if p.get("alphaxiv_overview"):
            continue
        ov = alphaxiv_source.fetch_overview(aid)
        if ov:
            p["alphaxiv_overview"] = ov["kind"]
            p["alphaxiv_video"] = alphaxiv_source.first_video(ov)[0]
            alphaxiv_source.write_overview_file(os.path.join(wd, "alphaxiv", f"{aid}.md"), aid, ov)
            new += 1
            print(f"  새로 받음: {aid}")
    _save_work(meta, date_str)
    have = sum(1 for aid in meta.get("top_ids", []) if by_id[aid].get("alphaxiv_overview"))
    print(f"alphaXiv 요약 {have}/{len(meta.get('top_ids', []))}편 (이번에 {new}편 추가)")


def cmd_check(args):
    """Schema + banned-word/style check over deep/*.json and synthesis.md. Exit 1 if anything is found."""
    meta, date_str = _load_work(args.date)
    wd = work_dir(date_str)
    by_id = {p["arxiv_id"]: p for p in meta["papers"]}
    problems = 0
    for aid in meta.get("top_ids", []):
        path = os.path.join(wd, "deep", f"{aid}.json")
        if not os.path.exists(path):
            print(f"[없음] {aid}: deep/{aid}.json 이 없음")
            problems += 1
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            print(f"[JSON 오류] {aid}: {e}")
            problems += 1
            continue
        need = DEEP_TEXT_FIELDS + ["score", "field"]
        if by_id[aid].get("alphaxiv_video"):
            need.append(DEEP_VIDEO_FIELD)
        if not by_id[aid].get("figure_source"):
            need.remove("figure_caption")
        missing = [k for k in need if not d.get(k)]
        if missing:
            print(f"[빈 칸] {aid}: {', '.join(missing)}")
            problems += 1
        for field, name, sugg, snip in style_check.check_deep(d):
            print(f"[{name}] {aid}.{field}: …{snip}… → {sugg}")
            problems += 1
    synth = os.path.join(wd, "synthesis.md")
    if os.path.exists(synth):
        with open(synth, "r", encoding="utf-8") as f:
            for name, sugg, snip in style_check.check_text(f.read()):
                print(f"[{name}] synthesis.md: …{snip}… → {sugg}")
                problems += 1
    else:
        print("[없음] synthesis.md")
        problems += 1
    print(f"CHECK: {problems}건")
    if problems:
        print("→ 지적된 문장만 고치고 다시 'check'. 실제 뜻으로 쓴 낱말(캐비닛을 닫음 등)은 그대로 둬도 됨.")
        sys.exit(1)


def _coerce_deep(d, fallback_score):
    try:
        d["score"] = max(0, min(100, int(d.get("score", 0))))
    except (TypeError, ValueError):
        d["score"] = fallback_score
    # 예전 스키마의 추정 학회 칸은 더 쓰지 않는다 (venue_detect 판정으로 대체)
    d.pop("venue", None)
    d.pop("venue_score", None)
    d.pop("venue_justification", None)
    if not isinstance(d.get("links"), dict):
        d["links"] = {}
    return d


def cmd_assemble(args):
    meta, date_str = _load_work(args.date)
    wd = work_dir(date_str)
    papers = meta["papers"]
    by_id = {p["arxiv_id"]: p for p in papers}

    top = []
    for pid in meta.get("top_ids", []):
        p = by_id[pid]
        deep_path = os.path.join(wd, "deep", f"{pid}.json")
        if os.path.exists(deep_path):
            try:
                with open(deep_path, "r", encoding="utf-8") as f:
                    p["deep"] = _coerce_deep(json.load(f), p["screen_score"])
                p["deep"]["text_source"] = p.get("text_source", "")
            except Exception as e:
                print(f"WARNING: {deep_path} 파싱 실패: {e}")
                p["deep"] = None
        else:
            print(f"WARNING: 정밀 리뷰 없음: {pid}")
            p["deep"] = None
        top.append(p)

    n_missing = sum(1 for p in top if not p.get("deep"))
    if n_missing and not args.allow_missing:
        print(f"→ {n_missing}편의 정밀 리뷰가 누락되었습니다. 채운 뒤 다시 실행하거나 --allow-missing으로 무시하세요.")
        sys.exit(1)

    def final_key(p):
        d = p.get("deep") or {}
        return (d.get("score", p["screen_score"]), p["robotics_relevance"], p["screen_score"])

    top.sort(key=final_key, reverse=True)

    synthesis_md = ""
    synth_path = os.path.join(wd, "synthesis.md")
    if os.path.exists(synth_path):
        with open(synth_path, "r", encoding="utf-8") as f:
            synthesis_md = f.read().strip()
    else:
        print("WARNING: synthesis.md 없음 — 트렌드 섹션이 빠집니다.")

    evaluator = args.evaluator
    seoul_now = datetime.now(pytz.timezone("Asia/Seoul"))
    report_md = pc.build_report_md(
        date_str, meta["weekday"], meta["category_counts"], meta["total_unique"],
        meta["evaluated"], top, papers, synthesis_md, evaluator, evaluator,
    )
    payload = {
        "date": date_str,
        "weekday": meta["weekday"],
        "generated_at": seoul_now.isoformat(),
        "categories": meta["categories"],
        "category_counts": meta["category_counts"],
        "total_new": meta["total_new"],
        "total_unique": meta["total_unique"],
        "evaluated": meta["evaluated"],
        "screen_model": evaluator,
        "deep_model": evaluator,
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
                "venue_info": p.get("venue_info") or {},
                "alphaxiv_url": alphaxiv_source.abs_url(p["arxiv_id"]),
                "alphaxiv_overview": p.get("alphaxiv_overview", ""),
                "alphaxiv_video": p.get("alphaxiv_video", ""),
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
            for p in sorted(papers, key=lambda x: (x["screen_score"], x["robotics_relevance"]), reverse=True)
        ],
        "synthesis_md": synthesis_md,
    }

    if args.dry_run:
        print("--dry-run: 저장 생략. 리포트 미리보기 (앞 2000자):")
        print(report_md[:2000])
        return

    os.makedirs(config.DAILY_DIR, exist_ok=True)
    with open(os.path.join(config.DAILY_DIR, f"{date_str}.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    with open(os.path.join(config.DAILY_DIR, f"{date_str}.md"), "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Saved database/daily/{date_str}.json / .md")

    # Prune before rendering: the generator only emits an <img> for figures that
    # exist on disk, so old archive pages lose their image slot in the same pass
    # instead of pointing at a deleted file.
    figure_extractor.prune()

    import static_generator

    static_generator.generate_static_html()

    seen = pc.load_seen_ids()
    pc.save_seen_ids(seen, [p["arxiv_id"] for p in papers], date_str)

    if not args.keep_work:
        shutil.rmtree(wd, ignore_errors=True)
        print(f"work 디렉토리 정리: {wd}")
    print("ASSEMBLED: git add/commit/push 후 GitHub Actions가 배포·노션 게시를 수행합니다.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("prepare", help="arXiv 수집 → 스크리닝 배치 생성")
    p1.add_argument("--force", action="store_true", help="이미 평가한 논문도 포함")
    p1.add_argument("--max-papers", type=int, default=None, help="(디버그) 논문 수 제한")
    p1.add_argument("--batch-size", type=int, default=25)
    p1.set_defaults(func=cmd_prepare)

    p2 = sub.add_parser("select", help="스크리닝 병합 → Top-K 선정 + PDF 텍스트 추출")
    p2.add_argument("--date", default=None)
    p2.add_argument("--top-k", type=int, default=config.TOP_K)
    p2.add_argument("--allow-missing", action="store_true")
    p2.set_defaults(func=cmd_select)

    p4 = sub.add_parser("alphaxiv", help="아직 없는 alphaXiv 요약을 다시 받아 봄")
    p4.add_argument("--date", default=None)
    p4.set_defaults(func=cmd_alphaxiv)

    p5 = sub.add_parser("check", help="정밀 리뷰·종합 스키마와 금지어·문체 검사")
    p5.add_argument("--date", default=None)
    p5.set_defaults(func=cmd_check)

    p3 = sub.add_parser("assemble", help="정밀 리뷰 병합 → 리포트·사이트 생성")
    p3.add_argument("--date", default=None)
    p3.add_argument("--allow-missing", action="store_true")
    p3.add_argument("--dry-run", action="store_true")
    p3.add_argument("--keep-work", action="store_true")
    p3.add_argument("--evaluator", default="Claude (scheduled agent)")
    p3.set_defaults(func=cmd_assemble)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
