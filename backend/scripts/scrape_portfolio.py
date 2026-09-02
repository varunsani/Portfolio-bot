"""
Scrapes Varun's live portfolio and writes it to content/portfolio.md, tagged
by section so the indexer can attach correct anchors/citations to every chunk.

This is what makes the knowledge base self-updating: run this on a schedule
(see .github/workflows/scrape-and-reindex.yml) and whenever the live site's
text changes, portfolio.md changes, which triggers reindex.yml.

Also extracts every external link referenced on the page (papers, GitHub
repos, chess games, F1 clips, etc.) into content/links.json so those get
indexed too.

Section detection is fully automatic -- no hardcoded heading map to maintain:
  1. Every `<section>`/`<article>`/`<footer>` with an `id="..."` on the page
     IS a section boundary (these are the HTML5 landmark tags — whichever one
     Varun happens to use for a given block). The id is
     used as the stable anchor (e.g. id="experience" -> "#experience"). These
     ids are wired to the nav bar's href="#..." links and to the page's own
     scroll-spy JS, so Varun can't quietly rename one without also breaking
     his own site navigation -- unlike decorative <h2> copy ("Race Stints"),
     which he changes on a whim for flavor.
  2. The friendly section label is read straight from the nav bar
     (<a href="#experience">Experience</a>). If a brand-new <section id="...">
     appears with no matching nav link yet, we humanize the id itself
     (e.g. "leadership" -> "Leadership") as a sane default label so indexing
     never breaks on a new section -- it just uses a plainer name until the
     nav catches up.
"""
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

PORTFOLIO_URL = "https://varunsani.vercel.app"
CONTENT_DIR = Path(__file__).parent.parent / "content"

DEFAULT_SECTION = ("Hero / Introduction", "#about")


def humanize(slug: str) -> str:
    """Fallback label for a section id with no nav entry, e.g. 'off-track' -> 'Off Track'."""
    return re.sub(r"[-_]+", " ", slug).strip().title()


def build_nav_labels(soup: BeautifulSoup) -> dict[str, str]:
    """Read id -> friendly label straight from the nav bar's in-page links."""
    labels: dict[str, str] = {}
    nav = soup.find("nav")
    if not nav:
        return labels
    for a in nav.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#"):
            text = a.get_text(" ", strip=True)
            if text:
                labels[href.lstrip("#")] = text
    return labels


def scrape() -> tuple[str, list[dict]]:
    resp = requests.get(PORTFOLIO_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Read nav labels before stripping anything, then remove script/style/svg noise.
    nav_labels = build_nav_labels(soup)
    for tag in soup(["script", "style", "svg"]):
        tag.decompose()

    body = soup.body or soup
    current_section, current_anchor = DEFAULT_SECTION
    markdown_lines = [f"# Varun Sani Portfolio\nSource: {PORTFOLIO_URL}\n"]
    links = {}

    for el in body.find_all(["section", "article", "footer", "h1", "h2", "h3", "h4", "p", "li", "a"]):
        # A <section>/<article>/<footer id="..."> boundary is authoritative,
        # regardless of what decorative heading copy lives inside it. (Varun's
        # contact block is a <footer id="contact">, not a <section> — HTML5
        # landmark tags in general carry the real anchors, not just <section>.)
        if el.name in ("section", "article", "footer"):
            section_id = el.get("id")
            if section_id:
                label = nav_labels.get(section_id, humanize(section_id))
                current_section, current_anchor = label, f"#{section_id}"
            continue

        text = el.get_text(" ", strip=True)
        if not text:
            continue

        if el.name in ("h1", "h2", "h3", "h4"):
            markdown_lines.append(f"\n## [{current_section}] {text}\n")
        elif el.name in ("p", "li"):
            markdown_lines.append(f"[{current_section}]({current_anchor}) {text}")

        if el.name == "a" and el.get("href", "").startswith("http"):
            href = el["href"]
            if PORTFOLIO_URL not in href:
                links[href] = {
                    "url": href,
                    "label": text,
                    "section": current_section,
                    "anchor": current_anchor,
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
