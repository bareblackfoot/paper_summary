"""arXiv daily new-submission collector.

Fetches the "New submissions" section of arXiv listing pages such as
https://arxiv.org/list/cs.CV/new for the configured categories.
Cross submissions (cross-lists) and replacement submissions are excluded.
Papers appearing in more than one category list are merged into one entry.
"""

import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import config

HEADERS = {"User-Agent": config.USER_AGENT}


def parse_listing_page(html):
    """Parse one arXiv /list/<cat>/new page.

    Returns (papers, declared_new_count, mailing_date):
      papers            – list of dicts, "New submissions" section only
      declared_new_count – the count arXiv declares in the section heading
      mailing_date      – datetime.date of the mailing, or None
    """
    soup = BeautifulSoup(html, "html.parser")

    mailing_date = None
    date_text = soup.find(string=re.compile(r"Showing new listings for"))
    if date_text:
        m = re.search(r"for\s+\w+,\s+(\d{1,2}\s+\w+\s+\d{4})", date_text)
        if m:
            try:
                mailing_date = datetime.strptime(m.group(1), "%d %B %Y").date()
            except ValueError:
                pass

    papers = []
    declared_new = None
    section = None
    pending_dt = None
    container = soup.find("div", id="dlpage") or soup

    # h3 section headings and dt/dd items appear in document order;
    # only items under the "New submissions" heading are collected.
    for tag in container.find_all(["h3", "dt", "dd"]):
        if tag.name == "h3":
            text = tag.get_text(" ", strip=True)
            if text.startswith("New submissions"):
                section = "new"
                m = re.search(r"of\s+(\d+)\s+entr", text)
                if m:
                    declared_new = int(m.group(1))
            elif text.startswith(("Cross submissions", "Replacement submissions")):
                section = "other"
            pending_dt = None
            continue

        if section != "new":
            continue

        if tag.name == "dt":
            pending_dt = tag
        elif tag.name == "dd" and pending_dt is not None:
            paper = _parse_item(pending_dt, tag)
            if paper:
                papers.append(paper)
            pending_dt = None

    return papers, declared_new, mailing_date


def _parse_item(dt, dd):
    link = dt.find("a", title="Abstract")
    if not link:
        return None
    arxiv_id = (link.get("id") or link.get_text(strip=True).replace("arXiv:", "")).strip()
    if not arxiv_id:
        return None

    def _field(cls, descriptor):
        div = dd.find("div", class_=cls)
        if not div:
            return ""
        return div.get_text(" ", strip=True).replace(descriptor, "", 1).strip()

    title = _field("list-title", "Title:")
    subjects = _field("list-subjects", "Subjects:")
    comments = _field("list-comments", "Comments:")

    authors = []
    authors_div = dd.find("div", class_="list-authors")
    if authors_div:
        authors = [a.get_text(strip=True) for a in authors_div.find_all("a")]

    primary = ""
    subj_div = dd.find("div", class_="list-subjects")
    if subj_div:
        prim = subj_div.find("span", class_="primary-subject")
        if prim:
            primary = prim.get_text(strip=True)

    abstract = ""
    abs_p = dd.find("p", class_="mathjax")
    if abs_p:
        abstract = abs_p.get_text(" ", strip=True)

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "subjects": subjects,
        "primary_subject": primary,
        "comments": comments,
        "abstract": abstract,
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
    }


def fetch_category(cat):
    """Fetch the new-submission list for one category."""
    url = config.ARXIV_LIST_URL.format(cat=cat)
    print(f"[arxiv] fetching {url}")
    resp = requests.get(url, headers=HEADERS, timeout=90)
    resp.raise_for_status()
    papers, declared, mailing_date = parse_listing_page(resp.text)
    if declared is not None and declared != len(papers):
        print(
            f"[arxiv] warning: {cat} declares {declared} new submissions "
            f"but {len(papers)} were parsed"
        )
    print(f"[arxiv] {cat}: {len(papers)} new submissions (mailing: {mailing_date})")
    return papers, mailing_date


def collect_new_submissions(categories=None):
    """Collect and deduplicate new submissions across categories.

    Returns (papers, category_counts, mailing_date):
      papers          – deduplicated list; each has "listed_in" (categories it
                        appeared in as a *new* submission)
      category_counts – per-category new-submission counts before dedup
      mailing_date    – datetime.date of the mailing (max across pages)
    """
    categories = categories or config.ARXIV_CATEGORIES
    merged = {}
    order = []
    category_counts = {}
    mailing_date = None

    for i, cat in enumerate(categories):
        if i > 0:
            time.sleep(config.ARXIV_REQUEST_DELAY)
        papers, cat_mailing = fetch_category(cat)
        category_counts[cat] = len(papers)
        if cat_mailing and (mailing_date is None or cat_mailing > mailing_date):
            mailing_date = cat_mailing
        for p in papers:
            pid = p["arxiv_id"]
            if pid in merged:
                if cat not in merged[pid]["listed_in"]:
                    merged[pid]["listed_in"].append(cat)
            else:
                p["listed_in"] = [cat]
                merged[pid] = p
                order.append(pid)

    papers = [merged[pid] for pid in order]
    total = sum(category_counts.values())
    print(
        f"[arxiv] total new submissions: {total} across {len(categories)} lists, "
        f"{len(papers)} unique after dedup"
    )
    return papers, category_counts, mailing_date


# ---------------------------------------------------------------------------
# Backfill: reconstruct a past mailing from /list/<cat>/recent
# ---------------------------------------------------------------------------


def _parse_recent_page(html, target_date, cat):
    """Items announced on target_date whose primary subject is `cat`.

    The /recent page keeps the last 5 mailings, grouped under date headings.
    A paper is a *new* submission for a category iff its primary subject is
    that category (cross-lists have a different primary) — verified against
    the /new page.
    """
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", id="dlpage") or soup
    papers = []
    cur_date = None
    pending_dt = None
    for tag in container.find_all(["h3", "dt", "dd"]):
        if tag.name == "h3":
            m = re.match(r"\w+,\s+(\d{1,2}\s+\w+\s+\d{4})", tag.get_text(" ", strip=True))
            cur_date = None
            if m:
                try:
                    cur_date = datetime.strptime(m.group(1), "%d %b %Y").date()
                except ValueError:
                    pass
            pending_dt = None
        elif tag.name == "dt":
            pending_dt = tag
        elif tag.name == "dd" and pending_dt is not None:
            if cur_date == target_date:
                p = _parse_item(pending_dt, tag)
                if p and f"({cat})" in p["primary_subject"]:
                    papers.append(p)
            pending_dt = None
    return papers


def _fetch_abstracts(papers, batch_size=100):
    """Fill in missing abstracts via the arXiv export API."""
    import xml.etree.ElementTree as ET

    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    missing = [p for p in papers if not p.get("abstract")]
    for i in range(0, len(missing), batch_size):
        batch = missing[i : i + batch_size]
        ids = ",".join(p["arxiv_id"] for p in batch)
        url = f"https://export.arxiv.org/api/query?id_list={ids}&max_results={len(batch)}"
        print(f"[arxiv] fetching {len(batch)} abstracts from export API")
        resp = requests.get(url, headers=HEADERS, timeout=120)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
        by_id = {}
        for entry in root.findall("atom:entry", ns):
            eid = (entry.findtext("atom:id", "", ns) or "").rsplit("/", 1)[-1]
            eid = re.sub(r"v\d+$", "", eid)
            summary = (entry.findtext("atom:summary", "", ns) or "").strip()
            comment = (entry.findtext("arxiv:comment", "", ns) or "").strip()
            by_id[eid] = (summary, comment)
        for p in batch:
            summary, comment = by_id.get(p["arxiv_id"], ("", ""))
            p["abstract"] = re.sub(r"\s+", " ", summary)
            if comment and not p.get("comments"):
                p["comments"] = comment
        time.sleep(config.ARXIV_REQUEST_DELAY)
    return papers


def collect_from_recent(target_date, categories=None):
    """Reconstruct the new submissions of a past mailing date.

    target_date: datetime.date — must be within the last ~5 mailings.
    Returns the same (papers, category_counts, mailing_date) as
    collect_new_submissions().
    """
    categories = categories or config.ARXIV_CATEGORIES
    merged = {}
    order = []
    category_counts = {}
    for i, cat in enumerate(categories):
        if i > 0:
            time.sleep(config.ARXIV_REQUEST_DELAY)
        url = f"https://arxiv.org/list/{cat}/recent?skip=0&show=2000"
        print(f"[arxiv] fetching {url} (backfill {target_date})")
        resp = requests.get(url, headers=HEADERS, timeout=90)
        resp.raise_for_status()
        papers = _parse_recent_page(resp.text, target_date, cat)
        category_counts[cat] = len(papers)
        print(f"[arxiv] {cat}: {len(papers)} new submissions on {target_date}")
        for p in papers:
            pid = p["arxiv_id"]
            if pid in merged:
                if cat not in merged[pid]["listed_in"]:
                    merged[pid]["listed_in"].append(cat)
            else:
                p["listed_in"] = [cat]
                merged[pid] = p
                order.append(pid)

    papers = [merged[pid] for pid in order]
    _fetch_abstracts(papers)
    total = sum(category_counts.values())
    print(
        f"[arxiv] backfill {target_date}: {total} new submissions, "
        f"{len(papers)} unique after dedup"
    )
    return papers, category_counts, target_date


if __name__ == "__main__":
    papers, counts, mailing = collect_new_submissions()
    print(f"mailing date: {mailing}")
    print(f"counts: {counts}")
    for p in papers[:5]:
        print(f"- {p['arxiv_id']} [{p['primary_subject']}] {p['title'][:80]}")
