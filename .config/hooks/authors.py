"""Authors hook for the CURIOSS patterns mkdocs site.

Reads ``authors.yml`` (slug -> {name, orcid, affiliation}) and per-pattern
``authors:`` frontmatter (list of slugs), then:

* Generates a single ``authors/index.md`` page with a roster table and one
  anchored section per author listing the patterns they've contributed to.
* Rewrites the ``## Contributors & Acknowledgement`` section in each pattern,
  replacing the legacy bullet list with links to anchors on the authors page
  while preserving any prose that follows the list.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import File

AUTHORS_FILE = "authors.yml"
ORCID_ICON = "assets/orcid-id.svg"
CONTRIB_HEADING_RE = re.compile(
    r"^##\s+Contributors\s*&\s*Acknowledg\w*\s*$",
    re.MULTILINE,
)
BULLET_LINE_RE = re.compile(r"^\s*[-*]\s+\S")
HEADING_RE = re.compile(r"^#+\s", re.MULTILINE)
FEED_SUMMARY_CHARS = 240

# Material for MkDocs hardcodes the autodiscovery <link rel="alternate"> tag
# to this filename. See .config/mkdocs.yml for context.
FEED_URL = "feed_rss_created.xml"
FEED_FILES = ("feed_rss_created.xml", "feed_rss_updated.xml")

# Validation regexes for authors.yml. Names and affiliations are interpolated
# into Markdown that allows inline HTML through, so we forbid characters that
# could open HTML tags. ORCIDs are interpolated into URLs and link bodies.
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
FORBIDDEN_IN_TEXT_RE = re.compile(r"[<>{}\x00-\x1f\x7f]")


def _validate_authors(data: dict) -> None:
    """Reject malformed or unsafe entries in authors.yml at build time.

    Names and affiliations later end up inside Markdown that allows raw HTML,
    and ORCIDs go into href attributes — so we strictly validate here rather
    than try to escape every downstream interpolation site.
    """
    for slug, record in data.items():
        loc = f"authors.yml: {slug!r}"
        if not isinstance(slug, str) or not SLUG_RE.match(slug):
            raise PluginError(
                f"{loc}: slug must match {SLUG_RE.pattern} "
                f"(lowercase letters, digits, hyphens)."
            )
        if not isinstance(record, dict):
            raise PluginError(f"{loc}: entry must be a mapping, got {type(record).__name__}.")
        name = record.get("name")
        if not isinstance(name, str) or not name.strip():
            raise PluginError(f"{loc}: 'name' is required and must be a non-empty string.")
        if FORBIDDEN_IN_TEXT_RE.search(name) or len(name) > 200:
            raise PluginError(
                f"{loc}: 'name' contains a forbidden character (<, >, {{, }} "
                f"or control char) or exceeds 200 chars."
            )
        aff = record.get("affiliation")
        if aff is not None:
            if not isinstance(aff, str):
                raise PluginError(f"{loc}: 'affiliation' must be a string.")
            if FORBIDDEN_IN_TEXT_RE.search(aff) or len(aff) > 300:
                raise PluginError(
                    f"{loc}: 'affiliation' contains a forbidden character or exceeds 300 chars."
                )
        orcid = record.get("orcid")
        if orcid is not None:
            if not isinstance(orcid, str) or not ORCID_RE.match(orcid):
                raise PluginError(
                    f"{loc}: 'orcid' must match {ORCID_RE.pattern} "
                    f"(e.g. 0000-0001-2345-6789). Got {orcid!r}."
                )


def _orcid_markdown(orcid: str, asset_prefix: str) -> str:
    """Render an ORCID iD with the official icon, wrapped in a link.

    ``asset_prefix`` is "" for source pages at the docs root and "../" for
    generated pages under ``authors/``.
    """
    icon = f"![ORCID iD icon]({asset_prefix}{ORCID_ICON})"
    return f"[{icon} {orcid}](https://orcid.org/{orcid})"


def _load_authors(docs_dir: str) -> dict:
    path = Path(docs_dir) / AUTHORS_FILE
    if not path.exists():
        raise PluginError(f"authors hook: {AUTHORS_FILE} not found at {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise PluginError(
            f"authors hook: {AUTHORS_FILE} must be a YAML mapping keyed by slug"
        )
    _validate_authors(data)
    return data


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].lstrip("\n")
    body = text[end + 4 :].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return {}, text
    return (fm if isinstance(fm, dict) else {}), body


def _read_authors_for_file(file: File) -> list[str]:
    if not file.abs_src_path or not file.src_path.endswith(".md"):
        return []
    try:
        text = Path(file.abs_src_path).read_text(encoding="utf-8")
    except OSError:
        return []
    fm, _ = _parse_frontmatter(text)
    raw = fm.get("authors") or []
    if not isinstance(raw, list):
        return []
    return [s for s in raw if isinstance(s, str)]


def _pattern_title(file: File) -> str:
    try:
        text = Path(file.abs_src_path).read_text(encoding="utf-8")
    except OSError:
        return Path(file.src_path).stem
    _, body = _parse_frontmatter(text)
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return Path(file.src_path).stem.replace("-", " ").title()


def _render_authors_index(
    authors_map: dict, by_author: dict[str, list[tuple[str, str]]]
) -> str:
    sorted_authors = sorted(
        authors_map.items(), key=lambda kv: kv[1].get("name", kv[0]).lower()
    )

    lines = [
        "# Authors",
        "",
        "Everyone who has contributed to a CURIOSS pattern. "
        "Click a name to jump to their entry below.",
        "",
        f'<p><em>New patterns are announced in the '
        f'<a href="../{FEED_URL}">RSS feed</a> — each item credits the authors '
        f'with a link to their ORCID profile.</em></p>',
        "",
        "| Author | Affiliation | ORCID |",
        "| --- | --- | --- |",
    ]
    for slug, record in sorted_authors:
        name = record.get("name", slug)
        aff = record.get("affiliation") or ""
        orcid = record.get("orcid")
        orcid_cell = _orcid_markdown(orcid, "../") if orcid else ""
        lines.append(f"| [{name}](#{slug}) | {aff} | {orcid_cell} |")

    for slug, record in sorted_authors:
        name = record.get("name", slug)
        aff = record.get("affiliation")
        orcid = record.get("orcid")
        lines += ["", f"## {name} {{ #{slug} }}", ""]
        if aff:
            lines += [f"**Affiliation:** {aff}", ""]
        if orcid:
            lines += [f"**ORCID:** {_orcid_markdown(orcid, '../')}", ""]
        lines += ["**Patterns:**", ""]
        patterns = by_author.get(slug, [])
        if patterns:
            for src_path, title in sorted(patterns, key=lambda p: p[1].lower()):
                lines.append(f"- [{title}](../{src_path})")
        else:
            lines.append("_No patterns yet._")
    lines.append("")
    return "\n".join(lines)


def _first_paragraph(markdown: str) -> str:
    """Return the first prose paragraph after the H1, stripped of markdown."""
    _, body = _parse_frontmatter(markdown)
    paragraphs: list[str] = []
    buf: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            if buf:
                paragraphs.append(" ".join(buf))
                buf = []
            continue
        if stripped.startswith("#") or BULLET_LINE_RE.match(line):
            if buf:
                paragraphs.append(" ".join(buf))
                buf = []
            continue
        buf.append(stripped)
    if buf:
        paragraphs.append(" ".join(buf))
    for p in paragraphs:
        plain = re.sub(r"[*_`]", "", p)
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
        if plain:
            return plain
    return ""


def _author_html(slug: str, record: dict) -> str:
    name = record.get("name", slug)
    orcid = record.get("orcid")
    name_safe = html.escape(name, quote=True)
    if orcid:
        # ORCID is validated against ORCID_RE at load time, so no characters
        # here need URL-encoding, but we still escape for attribute context.
        return (
            f'<a href="https://orcid.org/{html.escape(orcid, quote=True)}">{name_safe}</a>'
        )
    return name_safe


def _feed_description(slugs: list[str], authors_map: dict, markdown: str) -> str:
    """Build the HTML body for a feed item's <description>.

    Emitted as raw HTML (anchor tags, escaped text). The on_post_build hook
    later wraps each item-level <description> in CDATA so RSS readers render
    these as live links rather than as escaped text.
    """
    parts = [_author_html(slug, authors_map.get(slug, {"name": slug})) for slug in slugs]
    if not parts:
        attribution = ""
    elif len(parts) == 1:
        attribution = f"By {parts[0]}."
    else:
        attribution = "By " + ", ".join(parts[:-1]) + f", and {parts[-1]}."

    summary = _first_paragraph(markdown)
    if summary and len(summary) > FEED_SUMMARY_CHARS:
        summary = summary[: FEED_SUMMARY_CHARS - 1].rstrip() + "…"
    summary_html = html.escape(summary, quote=False) if summary else ""

    if attribution and summary_html:
        return f"{attribution} {summary_html}"
    return attribution or summary_html


def _render_pattern_bullets(slugs: list[str], authors_map: dict) -> str:
    bullets = []
    for slug in slugs:
        record = authors_map.get(slug, {})
        name = record.get("name", slug)
        aff = record.get("affiliation")
        orcid = record.get("orcid")
        line = f"- [{name}](authors/index.md#{slug})"
        extras = []
        if aff:
            extras.append(aff)
        if orcid:
            extras.append(_orcid_markdown(orcid, ""))
        if extras:
            line += " — " + ", ".join(extras)
        bullets.append(line)
    return "\n".join(bullets)


def on_files(files, config):
    authors_map = _load_authors(config["docs_dir"])

    by_author: dict[str, list[tuple[str, str]]] = {slug: [] for slug in authors_map}

    for f in list(files):
        if not f.is_documentation_page():
            continue
        if f.src_path.startswith("authors/"):
            continue
        slugs = _read_authors_for_file(f)
        if not slugs:
            continue
        title = _pattern_title(f)
        for slug in slugs:
            if slug not in authors_map:
                raise PluginError(
                    f"authors hook: pattern '{f.src_path}' references unknown "
                    f"author slug '{slug}'. Add an entry to {AUTHORS_FILE} or "
                    f"fix the slug."
                )
            by_author[slug].append((f.src_path, title))

    files.append(
        File.generated(
            config,
            "authors/index.md",
            content=_render_authors_index(authors_map, by_author),
        )
    )

    config["_authors_map"] = authors_map
    return files


def on_page_markdown(markdown, page, config, files):
    authors_map = config.get("_authors_map") or {}

    if page.file.src_path.startswith("authors/"):
        return markdown

    fm_authors = (page.meta or {}).get("authors") or []
    if not isinstance(fm_authors, list) or not fm_authors:
        return markdown

    resolved_names = [
        authors_map.get(slug, {}).get("name", slug) for slug in fm_authors
    ]
    page.meta["authors"] = resolved_names
    rss_meta = page.meta.setdefault("rss", {})
    if not rss_meta.get("feed_description"):
        rss_meta["feed_description"] = _feed_description(
            fm_authors, authors_map, markdown
        )

    rendered = _render_pattern_bullets(fm_authors, authors_map)

    m = CONTRIB_HEADING_RE.search(markdown)
    if not m:
        sep = "" if markdown.endswith("\n") else "\n"
        return (
            markdown
            + f"{sep}\n## Contributors & Acknowledgement\n\n{rendered}\n"
        )

    heading_end = m.end()
    next_h = HEADING_RE.search(markdown, heading_end + 1)
    section_end = next_h.start() if next_h else len(markdown)
    section_body = markdown[heading_end:section_end]

    body_lines = section_body.splitlines(keepends=True)
    i = 0
    while i < len(body_lines) and body_lines[i].strip() == "":
        i += 1
    while i < len(body_lines):
        line = body_lines[i]
        if BULLET_LINE_RE.match(line):
            i += 1
            continue
        if line.strip() == "" and i + 1 < len(body_lines) and BULLET_LINE_RE.match(
            body_lines[i + 1]
        ):
            i += 1
            continue
        break
    trailing = "".join(body_lines[i:])

    rebuilt = markdown[:heading_end] + "\n\n" + rendered + "\n"
    if trailing.strip():
        if not trailing.startswith("\n"):
            rebuilt += "\n"
        rebuilt += trailing
    rebuilt += markdown[section_end:]
    return rebuilt


# Pre-compiled patterns for the feed post-processor.
_ITEM_RE = re.compile(r"<item>.*?</item>", re.DOTALL)
_ITEM_DESC_RE = re.compile(r"<description>(.*?)</description>", re.DOTALL)
_AUTHOR_RE = re.compile(r"<author>(.*?)</author>", re.DOTALL)
_SOURCE_RE = re.compile(r"[ \t]*<source\b[^>]*>.*?</source>\s*\n?", re.DOTALL)
_CATEGORY_RE = re.compile(r"<category>(.*?)</category>", re.DOTALL)


def _rewrite_item(item_xml: str) -> str:
    """Apply per-item transforms inside a single <item>...</item> block."""

    def _desc_to_cdata(m: re.Match[str]) -> str:
        # The plugin HTML-escapes our description body; reverse that and
        # CDATA-wrap so feed readers render <a href="...">Name</a> as a real
        # link instead of as literal angle-bracket text.
        raw = html.unescape(m.group(1))
        # Defuse any literal "]]>" sequence that would close CDATA early.
        raw = raw.replace("]]>", "]]]]><![CDATA[>")
        return f"<description><![CDATA[{raw}]]></description>"

    item_xml = _ITEM_DESC_RE.sub(_desc_to_cdata, item_xml)
    # RSS 2.0 <author> must be an email address; use Dublin Core <dc:creator>
    # for plain names (the dc namespace is already declared by the plugin).
    item_xml = _AUTHOR_RE.sub(r"<dc:creator>\1</dc:creator>", item_xml)
    # The plugin emits a self-referencing <source> on every item. The RSS 2.0
    # spec reserves <source> for items republished from another feed, so we
    # strip it to keep the feed standards-compliant.
    item_xml = _SOURCE_RE.sub("", item_xml)
    # The plugin doesn't XML-escape category text, so tag names like
    # "Education & Skills" produce invalid XML. Re-escape defensively.
    item_xml = _CATEGORY_RE.sub(
        lambda m: f"<category>{html.escape(html.unescape(m.group(1)), quote=False)}</category>",
        item_xml,
    )
    return item_xml


def on_post_build(config):
    """Rewrite the generated feeds for spec compliance and link rendering.

    The mkdocs-rss-plugin has no template-override mechanism, so we patch
    its output after build: switch <author> to <dc:creator>, CDATA-wrap
    item descriptions so HTML renders, and drop self-referencing <source>.
    """
    site_dir = Path(config["site_dir"])
    for name in FEED_FILES:
        path = site_dir / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = _ITEM_RE.sub(lambda m: _rewrite_item(m.group(0)), text)
        path.write_text(text, encoding="utf-8")
