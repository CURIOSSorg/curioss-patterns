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

import re
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import File

AUTHORS_FILE = "authors.yml"
CONTRIB_HEADING_RE = re.compile(
    r"^##\s+Contributors\s*&\s*Acknowledg\w*\s*$",
    re.MULTILINE,
)
BULLET_LINE_RE = re.compile(r"^\s*[-*]\s+\S")
HEADING_RE = re.compile(r"^#+\s", re.MULTILINE)


def _load_authors(docs_dir: str) -> dict:
    path = Path(docs_dir) / AUTHORS_FILE
    if not path.exists():
        raise PluginError(f"authors hook: {AUTHORS_FILE} not found at {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise PluginError(
            f"authors hook: {AUTHORS_FILE} must be a YAML mapping keyed by slug"
        )
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
        "| Author | Affiliation | ORCID |",
        "| --- | --- | --- |",
    ]
    for slug, record in sorted_authors:
        name = record.get("name", slug)
        aff = record.get("affiliation") or ""
        orcid = record.get("orcid")
        orcid_cell = f"[{orcid}](https://orcid.org/{orcid})" if orcid else ""
        lines.append(f"| [{name}](#{slug}) | {aff} | {orcid_cell} |")

    for slug, record in sorted_authors:
        name = record.get("name", slug)
        aff = record.get("affiliation")
        orcid = record.get("orcid")
        lines += ["", f"## {name} {{ #{slug} }}", ""]
        if aff:
            lines += [f"**Affiliation:** {aff}", ""]
        if orcid:
            lines += [f"**ORCID:** [{orcid}](https://orcid.org/{orcid})", ""]
        lines += ["**Patterns:**", ""]
        patterns = by_author.get(slug, [])
        if patterns:
            for src_path, title in sorted(patterns, key=lambda p: p[1].lower()):
                lines.append(f"- [{title}](../{src_path})")
        else:
            lines.append("_No patterns yet._")
    lines.append("")
    return "\n".join(lines)


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
            extras.append(f"[ORCID](https://orcid.org/{orcid})")
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
