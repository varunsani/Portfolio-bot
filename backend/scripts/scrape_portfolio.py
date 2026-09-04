"""
Scrapes Varun's live portfolio and writes it to content/portfolio.md, tagged
by section so the indexer can attach correct anchors/citations to every chunk.

This is what makes the knowledge base self-updating: run this on a schedule
(see .github/workflows/scrape-and-reindex.yml) and whenever the live site's
text changes, portfolio.md changes, which triggers reindex.yml.

Section/anchor detection is fully automatic — no hardcoded section-name map
to maintain. The portfolio's own HTML already tags each block with a real
<section id="..."> / <footer id="..."> (that's what the nav's #anchor links
point at), plus an ".eyebrow" label and an <h2> inside each one for the
human-readable title. We read those directly, so renaming a section header
or adding a brand-new <section id="..."> on the live site is picked up on
the next scrape with zero changes needed here.

Also extracts every external link referenced on the page (papers, GitHub
repos, chess games, F1 clips, etc.) into content/links.json so those get
indexed too.
"""
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

PORTFOLIO_URL = "https://varunsani.vercel.app"
CONTENT_DIR = Path(__file__).parent.parent / "content"

ID_CONTAINER_TAGS = ["section", "footer", "header", "main", "article"]


def _container_title(container) -> str:
    """Human-readable section name, built from whatever the page itself
    uses to label the section (an '.eyebrow' tag and/or the first h1-h4),
    falling back to a title-cased version of the id if neither is present."""
    parts = []
    eyebrow = container.find(class_="eyebrow")
    if eyebrow:
        text = eyebrow.get_text(" ", strip=True)
        if text:
            parts.append(text)
    heading = container.find(["h1", "h2", "h3", "h4"])
    if heading:
        text = heading.get_text(" ", strip=True)
        if text:
            parts.append(text)
    if parts:
        return " — ".join(parts)
    return container.get("id", "section").replace("-", " ").replace("_", " ").title()


def _build_anchor_map(soup) -> list[tuple]:
    """Returns [(anchor, title, container), ...] in document order, for
    every real id-bearing section/footer/etc. on the page."""
    containers = soup.find_all(ID_CONTAINER_TAGS, id=True)
    return [(f"#{c['id']}", _container_title(c), c) for c in containers]


def _anchor_for(el, anchor_map, default_anchor, default_title):
    """Nearest ancestor (or self) with a real id wins. Content before the
    first id-bearing container (hero banner, intro strip, etc.) falls back
    to the first real section on the page, same as it visually leads into it."""
    node = el
    while node is not None:
        if getattr(node, "has_attr", None) and node.has_attr("id"):
            for anchor, title, container in anchor_map:
                if container is node:
                    return anchor, title
        node = node.parent
    return default_anchor, default_title


def scrape() -> tuple[str, list[dict]]:
    resp = requests.get(PORTFOLIO_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup(["script", "style", "nav", "svg"]):
        tag.decompose()

    body = soup.body or soup
    anchor_map = _build_anchor_map(soup)
    if anchor_map:
        default_anchor, default_title = anchor_map[0][0], anchor_map[0][1]
    else:
        default_anchor, default_title = "#about", "Introduction"

    markdown_lines = [f"# Varun Sani Portfolio\nSource: {PORTFOLIO_URL}\n"]
    links = {}
    seen_headings = set()

    for el in body.find_all(["h1", "h2", "h3", "h4", "p", "li", "a"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue

        anchor, section = _anchor_for(el, anchor_map, default_anchor, default_title)

        if el.name in ("h1", "h2", "h3", "h4"):
            key = (section, text)
            if key not in seen_headings:
                seen_headings.add(key)
                markdown_lines.append(f"\n## [{section}] {text}\n")
        elif el.name in ("p", "li"):
            markdown_lines.append(f"[{section}]({anchor}) {text}")

        if el.name == "a" and el.get("href", "").startswith("http"):
            href = el["href"]
            if PORTFOLIO_URL not in href:
                links[href] = {
                    "url": href,
                    "label": text,
                    "section": section,
                    "anchor": anchor,
                }

    markdown = "\n".join(markdown_lines)
    return markdown, list(links.values())


def main():
    CONTENT_DIR.mkdir(exist_ok=True)
    markdown, links = scrape()

    portfolio_path = CONTENT_DIR / "portfolio.md"
    links_path = CONTENT_DIR / "links.json"

    old_markdown = portfolio_path.read_text() if portfolio_path.exists() else ""
    changed = old_markdown.strip() != markdown.strip()

    portfolio_path.write_text(markdown)
    links_path.write_text(json.dumps(links, indent=2))

    # Signal to the calling GitHub Action whether content actually changed,
    # so we don't reindex (and burn embedding compute) on no-op runs.
    if changed:
        print("CHANGED")
        sys.exit(0)
    else:
        print("UNCHANGED")
        sys.exit(0)


if __name__ == "__main__":
    main()
