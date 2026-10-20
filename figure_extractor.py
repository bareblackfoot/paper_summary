"""Pull one representative figure per Top-K paper for the daily report cards.

Everything is fetched from arxiv.org, so the cloud sandbox's domain allowlist
covers it without opening the run up to arbitrary project-page hosts.

Three attempts, best first:
  1. the LaTeXML HTML edition's first real figure image
  2. the largest raster image embedded in the PDF's opening pages
  3. a render of the largest vector-drawing cluster on those pages

Papers where all three come up empty simply get no figure; the card template
drops the image slot for them.
"""

import io
import os
import re
import time
from urllib.parse import urljoin

import requests

import config

HEADERS = {"User-Agent": config.USER_AGENT}

MAX_WIDTH = 1000  # stored width; matches the card's inner width so figures can fill it
WEBP_QUALITY = 78
MIN_PIXELS = 40_000  # drops logos, ORCID marks, and similar chrome
MAX_ASPECT = 1.4  # taller than this gets cropped to the top (diagram over caption)
PDF_SCAN_PAGES = 3
MIN_PDF_IMAGE_AREA = 12_000  # in PDF points^2
MIN_HTML_IMG_WIDTH = 200  # narrower than this is a thumbnail, not a figure


def _log(msg):
    print(f"[figure] {msg}")


# --- saving -----------------------------------------------------------------


def _save(raw, out_path):
    """Normalise raw image bytes to a card-sized WebP. Returns True if written."""
    from PIL import Image

    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
    except Exception as e:
        _log(f"decode failed: {e}")
        return False

    if im.mode in ("RGBA", "LA", "P"):
        rgba = im.convert("RGBA")
        flat = Image.new("RGB", rgba.size, "white")
        flat.paste(rgba, mask=rgba.split()[-1])
        im = flat
    else:
        im = im.convert("RGB")

    if im.width * im.height < MIN_PIXELS:
        return False

    if im.height > im.width * MAX_ASPECT:
        im = im.crop((0, 0, im.width, int(im.width * MAX_ASPECT)))

    if im.width > MAX_WIDTH:
        height = max(1, round(im.height * MAX_WIDTH / im.width))
        im = im.resize((MAX_WIDTH, height), Image.LANCZOS)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path, "WEBP", quality=WEBP_QUALITY, method=6)
    return True


# --- source 1: arXiv HTML ---------------------------------------------------


def _looks_like_chrome(src):
    return bool(re.search(r"(logo|orcid|icon|badge|ar5iv)", src, re.I))


def _candidate_urls(page_url, src):
    """arXiv writes img src relative to /html/, but not every paper does.

    e.g. "2608.21204v1/img/teaser.png" resolves against the page URL itself,
    while a bare "x1.png" resolves against the paper's own directory. Try both
    rather than guessing.
    """
    if src.startswith(("http://", "https://")):
        return [src]
    out = []
    for base in (page_url, page_url.rstrip("/") + "/"):
        url = urljoin(base, src)
        if url not in out:
            out.append(url)
    return out


def _declared_size(img):
    """LaTeXML stamps width/height on every <img>, which is enough to skip
    thumbnail grids without downloading them. Returns None when absent."""
    try:
        w, h = int(img.get("width") or 0), int(img.get("height") or 0)
    except ValueError:
        return None
    return (w, h) if w and h else None


def _download_img(page_url, img):
    for candidate in _candidate_urls(page_url, img["src"]):
        try:
            r = requests.get(candidate, headers=HEADERS, timeout=60)
        except Exception:
            continue
        if r.ok and r.headers.get("Content-Type", "").startswith("image/") and len(r.content) > 4000:
            return r.content
    return None


def _pick_from_figure(fig):
    """The best <img> in one figure, or None if it only holds thumbnails.

    A teaser built from a strip of sample frames (Figure 1 of some papers is
    ten 43x33 stills) reads as noise on a card, so those are passed over in
    favour of a later, larger diagram.
    """
    imgs = [
        i for i in fig.find_all("img")
        if i.get("src") and not _looks_like_chrome(i["src"])
    ]
    if not imgs:
        return None, None
    sized = [(i, _declared_size(i)) for i in imgs]
    known = [(i, d) for i, d in sized if d]
    if not known:
        return imgs[0], None  # no metadata: take it and let _save judge
    img, (w, h) = max(known, key=lambda t: t[1][0] * t[1][1])
    return img, (w >= MIN_HTML_IMG_WIDTH)


def _from_html(arxiv_id):
    from bs4 import BeautifulSoup

    for suffix in ("v1", ""):
        url = f"https://arxiv.org/html/{arxiv_id}{suffix}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
        except Exception as e:
            _log(f"{arxiv_id}: HTML fetch failed: {e}")
            continue
        if not r.ok or "<figure" not in r.text:
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        # Subfigures are <figure> too; only walk the outer ones so a figure is
        # considered as a whole.
        tops = [f for f in soup.find_all("figure") if not f.find_parent("figure")]

        undersized = []
        for fig in tops:
            img, big_enough = _pick_from_figure(fig)
            if img is None:
                continue
            if big_enough is False:
                undersized.append(img)
                continue
            raw = _download_img(r.url, img)
            if raw:
                return raw, "arXiv HTML"

        # every figure was a thumbnail strip — better than nothing
        for img in undersized:
            raw = _download_img(r.url, img)
            if raw:
                return raw, "arXiv HTML"
    return None, None


# --- source 2 & 3: the PDF --------------------------------------------------


def _largest_embedded_image(doc):
    import fitz

    best_area, best_xref = 0, None
    for pno in range(min(PDF_SCAN_PAGES, doc.page_count)):
        for info in doc[pno].get_image_info(xrefs=True):
            xref = info.get("xref")
            if not xref:
                continue
            area = fitz.Rect(info["bbox"]).get_area()
            if area > best_area and area >= MIN_PDF_IMAGE_AREA:
                best_area, best_xref = area, xref
    if best_xref:
        try:
            return doc.extract_image(best_xref)["image"]
        except Exception as e:
            _log(f"embedded image extract failed: {e}")
    return None


def _cluster(rects, gap=12):
    """Greedily merge rectangles that touch or nearly touch."""
    import fitz

    clusters = []
    for r in rects:
        r = fitz.Rect(r)
        if r.is_empty or r.is_infinite:
            continue
        merged = r
        rest = []
        for c in clusters:
            probe = fitz.Rect(merged)
            probe += (-gap, -gap, gap, gap)
            if probe.intersects(c):
                merged |= c
            else:
                rest.append(c)
        rest.append(merged)
        clusters = rest
    return clusters


def _render_vector_figure(doc):
    import fitz

    for pno in range(min(PDF_SCAN_PAGES, doc.page_count)):
        page = doc[pno]
        rects = [d["rect"] for d in page.get_drawings()]
        if not rects:
            continue
        pw, ph = page.rect.width, page.rect.height
        candidates = [
            c
            for c in _cluster(rects)
            if c.width > pw * 0.35 and c.height > ph * 0.12
        ]
        if not candidates:
            continue
        clip = max(candidates, key=lambda c: c.get_area())
        clip += (-6, -6, 6, 6)
        clip &= page.rect
        try:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip)
            return pix.tobytes("png")
        except Exception as e:
            _log(f"vector render failed: {e}")
    return None


def _from_pdf(arxiv_id):
    import fitz

    try:
        r = requests.get(f"https://arxiv.org/pdf/{arxiv_id}", headers=HEADERS, timeout=180)
        r.raise_for_status()
        doc = fitz.open(stream=r.content, filetype="pdf")
    except Exception as e:
        _log(f"{arxiv_id}: PDF fetch failed: {e}")
        return None, None

    with doc:
        raw = _largest_embedded_image(doc)
        if raw:
            return raw, "PDF 이미지"
        raw = _render_vector_figure(doc)
        if raw:
            return raw, "PDF 렌더"
    return None, None


# --- entry points -----------------------------------------------------------


def figure_path(date_str, arxiv_id):
    return os.path.join("static", "figures", date_str, f"{arxiv_id}.webp")


def fetch_figure(arxiv_id, date_str, delay=True):
    """Store one representative figure. Returns the source label, or None."""
    out_path = figure_path(date_str, arxiv_id)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 2000:
        return "기존 파일"

    for attempt in (_from_html, _from_pdf):
        raw, label = attempt(arxiv_id)
        if raw and _save(raw, out_path):
            return label
        if delay:
            time.sleep(config.ARXIV_REQUEST_DELAY)
    return None


def prune(keep_days=None):
    """Drop figure directories older than the retention window."""
    import shutil
    from datetime import date, timedelta

    keep_days = keep_days or config.FIGURE_KEEP_DAYS
    root = os.path.join("static", "figures")
    if not os.path.isdir(root):
        return
    cutoff = (date.today() - timedelta(days=keep_days)).isoformat()
    for name in sorted(os.listdir(root)):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", name) and name < cutoff:
            shutil.rmtree(os.path.join(root, name), ignore_errors=True)
            _log(f"pruned {name}")
