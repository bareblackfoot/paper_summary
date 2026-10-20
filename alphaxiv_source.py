"""alphaXiv에서 Top-K 논문의 AI 요약(overview)을 받아 온다.

alphaXiv는 논문마다 사람이 읽기 좋은 요약 글(blog 형식, 그림·캡션 포함)을 만든다.
이 글은 누군가 alphaXiv에서 그 논문을 열어 요청해야 생기므로 갓 올라온 논문에는
대개 없다. 있으면 정밀 리뷰의 참고 자료로 쓰고, 없어도 링크는 항상 건다.

  https://www.alphaxiv.org/abs/<id>        논문 페이지 (링크용)
  https://www.alphaxiv.org/overview/<id>   요약 글 (없으면 /abs/<id>로 redirect)
  https://www.alphaxiv.org/overview/<id>.md 요약 보고서 markdown (없으면 404)

요약 글은 서버 렌더된 HTML의 `.blog-post` 안에 있다. 로그인 없이 읽을 수 있는 것은
이미 만들어진 요약뿐이다 (생성 요청 API는 로그인 필요).
"""

import re

import requests

import config

HEADERS = {"User-Agent": config.USER_AGENT}
BASE = "https://www.alphaxiv.org"


def abs_url(arxiv_id):
    return f"{BASE}/abs/{arxiv_id}"


def overview_url(arxiv_id):
    return f"{BASE}/overview/{arxiv_id}"


def _text(node):
    """Element text with KaTeX collapsed to its TeX source."""
    for k in node.select(".katex"):
        ann = k.find("annotation")
        k.replace_with(f"${ann.get_text().strip()}$" if ann else k.get_text(" ", strip=True))
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()


def _blog_to_markdown(blog):
    """Turn the rendered `.blog-post` element into markdown text + figure list."""
    lines, figures = [], []
    for el in blog.find_all(["h1", "h2", "h3", "p", "li", "figure"], recursive=True):
        # text inside a figure or a list item is emitted with that container
        if el.name != "figure" and el.find_parent(["figure", "li"]) is not None:
            continue
        if el.name == "figure":
            img = el.find("img")
            video = el.find("video")
            src = video.find("source") if video is not None and not video.get("src") else None
            cap = el.find("figcaption")
            fig = {
                "type": "video" if video is not None else "image",
                "url": (video.get("src") or (src.get("src") if src else "")) if video is not None
                else (img.get("src", "") if img else ""),
                "page": img.get("data-paper-page", "") if img else "",
                "caption": _text(cap) if cap else "",
            }
            figures.append(fig)
            kind = "영상" if fig["type"] == "video" else "그림"
            where = f" (원문 {fig['page']}쪽)" if fig["page"] else ""
            lines.append(f"\n[{kind} {len(figures)}]{where} {fig['caption']}\n")
            continue
        t = _text(el)
        if not t:
            continue
        if el.name in ("h1", "h2", "h3"):
            lines.append(f"\n## {t}\n")
        elif el.name == "li":
            lines.append(f"- {t}")
        else:
            lines.append(t + "\n")
    return "\n".join(lines).strip(), figures


def fetch_overview(arxiv_id, timeout=40):
    """Return {"kind", "text", "figures", "url"} or None when alphaXiv has no summary.

    kind = "blog"   — the rendered overview article (preferred; what a reader sees)
           "report" — the longer markdown report, used when only that exists
    Raises nothing: network errors are reported as None with a printed note so a
    blocked domain never stops the pipeline.
    """
    try:
        from bs4 import BeautifulSoup

        r = requests.get(overview_url(arxiv_id), headers=HEADERS, timeout=timeout)
        if r.ok:  # alphaXiv redirects to /abs/<id>; the article is embedded there when it exists
            blog = BeautifulSoup(r.text, "html.parser").select_one(".blog-post")
            if blog is not None:
                text, figures = _blog_to_markdown(blog)
                if len(text) > 500:
                    return {"kind": "blog", "text": text, "figures": figures, "url": overview_url(arxiv_id)}
        r = requests.get(f"{overview_url(arxiv_id)}.md", headers=HEADERS, timeout=timeout)
        if r.ok and len(r.text) > 500 and "text/markdown" in r.headers.get("content-type", ""):
            return {"kind": "report", "text": r.text.strip(), "figures": [], "url": overview_url(arxiv_id)}
    except Exception as e:
        print(f"[alphaxiv] {arxiv_id}: 받기 실패 ({type(e).__name__}: {e})")
    return None


def fetch_fulltext(arxiv_id, timeout=60):
    """alphaXiv's extracted full text (markdown). Used only when arXiv PDF/HTML both fail."""
    try:
        r = requests.get(f"{BASE}/abs/{arxiv_id}.md", headers=HEADERS, timeout=timeout)
        if r.ok and len(r.text) > 2000:
            return r.text
    except Exception as e:
        print(f"[alphaxiv] {arxiv_id}: 전문 받기 실패 ({type(e).__name__}: {e})")
    return None


def reachable(timeout=15):
    """True if alphaxiv.org answers at all (egress check for the cloud sandbox)."""
    try:
        # a sandbox proxy that blocks the domain answers 403, so only a real 200 counts
        return requests.get(f"{BASE}/abs/2610.13816.md", headers=HEADERS, timeout=timeout).status_code == 200
    except Exception:
        return False


def write_overview_file(path, arxiv_id, ov):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# alphaXiv 요약 ({'요약 글' if ov['kind'] == 'blog' else '요약 보고서'})\n")
        f.write(f"출처: {ov['url']}\n\n")
        f.write(ov["text"])
        if ov["figures"]:
            f.write("\n\n## alphaXiv가 고른 그림·영상\n")
            for i, fig in enumerate(ov["figures"], 1):
                kind = "영상" if fig.get("type") == "video" else "그림"
                where = f" (원문 {fig['page']}쪽)" if fig.get("page") else ""
                f.write(f"- {kind} {i}{where}: {fig['caption']}\n  {fig['url']}\n")


def first_video(ov):
    """(url, english caption) of the first video in an overview, or ("", "")."""
    for fig in (ov or {}).get("figures", []):
        if fig.get("type") == "video" and fig.get("url"):
            return fig["url"], fig.get("caption", "")
    return "", ""
