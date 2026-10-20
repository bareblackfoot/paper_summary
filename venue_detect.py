"""논문이 어느 학회에 나갔거나 나갈지, 근거와 함께 판정한다.

LLM이 «잘 맞을 학회»를 추측하던 칸(venue)을 대신한다. 세 단계로 보고, 앞 단계에서
나오면 뒤는 보지 않는다.

  1. arXiv comments 의 명시      "Accepted at CoRL 2026", "Submitted to ICRA 2027"
  2. PDF에 박힌 학회 문구       "10th Conference on Robot Learning (CoRL 2026)" 꼬리말,
                                 "Under review as a conference paper at ICLR 2027" 머리글
  3. LaTeX 양식으로 추정         ICLR(제목 전부 대문자), NeurIPS(1쪽 꼬리말 'Preprint.'),
                                 IEEE 2단('Abstract—'), CoRL(초록 아래 'Keywords:') 등

결과는 {"venue", "status", "basis", "evidence"}:
  venue    학회 이름 (연도 있으면 붙임). 판정 못 하면 ""
  status   "채택" | "투고" | "양식 추정" | ""
  basis    "comments" | "PDF 문구" | "양식"
  evidence 화면에 그대로 보여 줄 근거 한 줄 (원문 인용 또는 양식 특징)
"""

import io
import re

# (정규식 이름, 표시 이름). 긴 이름을 먼저 둔다 (RA-L 이 ICRA 보다 먼저 잡히게).
VENUES = [
    (r"Conference on Robot Learning|CoRL", "CoRL"),
    (r"Neural Information Processing Systems|NeurIPS|NIPS", "NeurIPS"),
    (r"International Conference on Learning Representations|ICLR", "ICLR"),
    (r"International Conference on Machine Learning|ICML", "ICML"),
    (r"Robotics:? Science and Systems|\bRSS\b", "RSS"),
    (r"Robotics and Automation Letters|RA-?L\b", "RA-L"),
    (r"International Conference on Robotics and Automation|ICRA", "ICRA"),
    (r"Intelligent Robots and Systems|IROS", "IROS"),
    (r"Computer Vision and Pattern Recognition|CVPR", "CVPR"),
    (r"International Conference on Computer Vision|ICCV", "ICCV"),
    (r"European Conference on Computer Vision|ECCV", "ECCV"),
    (r"\bWACV\b", "WACV"),
    (r"\b3DV\b", "3DV"),
    (r"\bAAAI\b", "AAAI"),
    (r"\bIJCAI\b", "IJCAI"),
    (r"\bEMNLP\b", "EMNLP"),
    (r"\bNAACL\b", "NAACL"),
    (r"\bACL\b", "ACL"),
    (r"\bCOLM\b", "COLM"),
    (r"\bAISTATS\b", "AISTATS"),
    (r"\bUAI\b", "UAI"),
    (r"Transactions on Machine Learning Research|\bTMLR\b", "TMLR"),
    (r"Transactions on Robotics|\bT-RO\b", "T-RO"),
    (r"\bIJRR\b|International Journal of Robotics Research", "IJRR"),
    (r"\bHumanoids\b", "Humanoids"),
    (r"\bHRI\b", "HRI"),
    (r"\bL4DC\b", "L4DC"),
]

ACCEPT = r"accepted|to appear|camera[- ]ready|published|spotlight|oral|poster|in proceedings|proceedings of"
SUBMIT = r"submitted|under review|in submission|under submission|submission to"


def _venue_name(text):
    for pat, name in VENUES:
        m = re.search(pat, text, re.I if name not in ("RSS", "ACL", "UAI", "HRI") else 0)
        if m:
            year = re.search(r"(?<!\d)(20\d\d)(?!\d)|'(\d\d)\b", text[m.start():m.start() + 80])
            if year:
                y = year.group(1) or f"20{year.group(2)}"
                return f"{name} {y}"
            return name
    return ""


def from_comments(comments):
    c = (comments or "").strip()
    if not c:
        return None
    venue = _venue_name(c)
    if not venue:
        return None
    if re.search(SUBMIT, c, re.I):
        status = "투고"
    elif re.search(ACCEPT, c, re.I):
        status = "채택"
    else:
        # "8 pages, ICRA" 처럼 학회 이름만 적힌 경우: 채택인지 투고인지 모름
        status = "표기"
    return {"venue": venue, "status": status, "basis": "comments", "evidence": f"comments에 \"{c[:160]}\""}


# PDF에 박힌 문구. (정규식, 상태, 학회 이름 만드는 함수)
_PDF_PHRASES = [
    (r"Published as a conference paper at (ICLR \d{4})", "채택", lambda m: m.group(1)),
    (r"Under review as a conference paper at (ICLR \d{4})", "투고", lambda m: m.group(1)),
    (r"\d+(?:st|nd|rd|th) Conference on Neural Information Processing Systems \((NeurIPS \d{4})\)", "채택", lambda m: m.group(1)),
    (r"Submitted to (?:the )?\d+(?:st|nd|rd|th) Conference on Neural Information", "투고", lambda m: "NeurIPS"),
    (r"Submitted to (?:the )?\d+(?:st|nd|rd|th) Conference on Robot Learning \((CoRL \d{4})\)", "투고", lambda m: m.group(1)),
    (r"\d+(?:st|nd|rd|th) Conference on Robot Learning \((CoRL \d{4})\)", "채택", lambda m: m.group(1)),
    (r"Proceedings of the \d+(?:st|nd|rd|th) International Conference on Machine\s+Learning[^\n]{0,60}?(20\d\d)", "채택", lambda m: f"ICML {m.group(1)}"),
    (r"Under review by the International Conference on Machine Learning", "투고", lambda m: "ICML"),
    (r"Robotics: Science and Systems (20\d\d)", "채택", lambda m: f"RSS {m.group(1)}"),
    (r"Published in Transactions on Machine Learning Research", "채택", lambda m: "TMLR"),
    (r"Under review as submission to TMLR", "투고", lambda m: "TMLR"),
    (r"(CVPR|ICCV|WACV) (20\d\d) Submission #", "투고", lambda m: f"{m.group(1)} {m.group(2)}"),
    (r"Confidential Review Copy\. DO NOT DISTRIBUTE", "투고", lambda m: "CVPR·ICCV 계열"),
    (r"Copyright © (20\d\d), Association for the Advancement of Artificial Intelligence", "채택", lambda m: f"AAAI {int(m.group(1))}"),
    (r"IEEE Robotics and Automation Letters", "표기", lambda m: "RA-L"),
]


def _first_page_info(pdf_bytes):
    """First-page lines, page-1 footer lines, column count, full text (all pages)."""
    import fitz  # pymupdf

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    width = page.rect.width
    mid = width / 2
    blocks = [b for b in page.get_text("blocks") if b[6] == 0]
    left = sum(1 for b in blocks if b[2] < mid + 5 and len(b[4]) > 80)
    fonts = set()
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln["spans"]:
                fonts.add(sp["font"].split("+")[-1])
    right = sum(1 for b in blocks if b[0] > mid - 5 and (b[2] - b[0]) < width * 0.55 and len(b[4]) > 80)
    lines = [l.strip() for l in page.get_text().split("\n") if l.strip()]
    lines = [l for l in lines if not l.startswith("arXiv:")]
    full = "\n".join(p.get_text() for p in doc)
    return {
        "lines": lines,
        "two_column": left >= 1 and right >= 1,
        "fonts": fonts,
        "pages": len(doc),
        "full": full,
        "a4": abs(page.rect.height - 842) < 4,
    }


HEADER_LINE = r"(?i)^(preprint|under review|pre-print)[\s.,]*(under review[\s.]*)?$|^\d+$|^\d{4}-\d\d-\d\d$"


def _caps_title(lines):
    """ICLR style: the title is set in capitals.

    Some PDFs repeat the title in normal case on the first line (hidden metadata
    text), so a capitals line anywhere in the first five non-header lines counts.
    """
    head = [l for l in lines[:8] if not re.match(HEADER_LINE, l)][:5]
    for l in head:
        letters = re.sub(r"[^A-Za-z]", "", l)
        if len(letters) >= 12 and letters.isupper():
            return True
    return False


def from_pdf(pdf_bytes):
    try:
        info = _first_page_info(pdf_bytes)
    except Exception as e:
        print(f"[venue] PDF 읽기 실패: {e}")
        return None
    first = "\n".join(info["lines"])
    for pat, status, name in _PDF_PHRASES:
        m = re.search(pat, first)
        if m:
            return {"venue": name(m), "status": status, "basis": "PDF 문구",
                    "evidence": f"1쪽에 \"{m.group(0)[:120]}\""}
    if re.search(r"NeurIPS Paper Checklist", info["full"], re.I):
        return {"venue": "NeurIPS", "status": "양식 추정", "basis": "양식",
                "evidence": "부록에 NeurIPS Paper Checklist 있음"}

    lines = info["lines"]
    tail = lines[-3:]
    has_keywords = any(re.match(r"^Keywords:", l) for l in lines)
    ieee_abstract = re.search(r"Abstract\s*[—–-]\s*\S", first) is not None
    if _caps_title(lines) and not info["two_column"]:
        return {"venue": "ICLR", "status": "양식 추정", "basis": "양식",
                "evidence": "제목 전체 대문자, 1단 구성"}
    if not info["two_column"] and has_keywords:
        return {"venue": "CoRL", "status": "양식 추정", "basis": "양식",
                "evidence": "1단 구성, 초록 아래 'Keywords:' 줄"}
    if not info["two_column"] and any(re.match(r"^Preprint\.?( Under review\.?)?$", l) for l in tail):
        return {"venue": "NeurIPS", "status": "양식 추정", "basis": "양식",
                "evidence": "1단 구성, 1쪽 꼬리말 'Preprint.'"}
    if info["two_column"] and ieee_abstract:
        if info["pages"] > 12:
            return {"venue": "IEEE 학술지 계열", "status": "양식 추정", "basis": "양식",
                    "evidence": f"IEEE 2단 양식, {info['pages']}쪽"}
        return {"venue": "ICRA·IROS·RA-L 계열", "status": "양식 추정", "basis": "양식",
                "evidence": f"IEEE 2단 양식, {info['pages']}쪽"}
    for font, org in (("OptimisticDisp", "Meta"), ("ByteSans", "ByteDance")):
        if any(f.startswith(font) for f in info["fonts"]):
            return {"venue": f"{org} 자체 양식", "status": "양식 추정", "basis": "양식",
                    "evidence": f"글꼴 {font}, 학회 양식 아님"}
    if info["two_column"] and info["a4"]:
        return {"venue": "ACL 계열", "status": "양식 추정", "basis": "양식",
                "evidence": "A4 용지, 2단 구성"}
    return None


def detect(comments, pdf_bytes=None):
    """comments 명시 → PDF 문구 → 양식 순. 아무것도 없으면 빈 판정."""
    c = from_comments(comments)
    if c and c["status"] in ("채택", "투고"):
        return c
    p = from_pdf(pdf_bytes) if pdf_bytes else None
    if p and p["basis"] == "PDF 문구":
        return p
    if c:  # comments 에 학회 이름만 있음
        return c
    if p:
        return p
    return {"venue": "", "status": "", "basis": "", "evidence": ""}


def label(v):
    """카드에 붙일 짧은 표시. 예: 'CoRL 2026 채택', 'ICLR 양식 (추정)'."""
    if not v or not v.get("venue"):
        return ""
    if v["status"] == "양식 추정":
        if v["venue"].endswith("양식"):
            return v["venue"]
        return f"{v['venue']} 양식 (추정)"
    if v["status"] == "표기":
        return f"{v['venue']} (comments 표기)"
    return f"{v['venue']} {v['status']}"
