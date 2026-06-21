#!/usr/bin/env python3
"""
render-doc-pdf.py — Markdown → branded PDF report renderer.

Turns a Markdown file (with optional YAML frontmatter) into a polished PDF with a
dark cover / title page, accent-coloured headings, severity-friendly tables and a
running footer. Colours, the logo badge letter and the org name come from a small
branding JSON, so the same engine themes any brand without touching the template.

Usage:
    python3 render-doc-pdf.py report.md
    python3 render-doc-pdf.py report.md --out custom.pdf
    python3 render-doc-pdf.py report.md --brand ../branding/examples/acme-capital.json
    python3 render-doc-pdf.py reports/            # render every .md in a folder

Recognized frontmatter keys (all optional):
    title:    Document title (defaults to first H1 in body, then filename).
    subtitle: One-line description under the title on the cover.
    kind:     audit|plan|report|reference|memo|rfc|agent-spec  (defaults: report)
    status:   draft|final|review|archived  (defaults: draft)
    date:     ISO date string (defaults to today)
    author:   Author name/handle
    app:      Subject / product / application name (cover "Application" field)
    org:      Org name on the cover (defaults to the branding name)
    org_tld:  Domain under the org name (defaults to the branding org_tld)
    mark:     Single-character logo badge on the cover (defaults to the branding mark)
    brand:    Path to a brand JSON overriding per-document branding
              (default: auto-discover ../branding/report-brand.json next to this repo).

Branding:
    The template ships sensible defaults; a brand JSON (schema:
    branding/report-brand.schema.json) overrides colours, the badge letter and the
    org name. Resolution precedence: --brand > frontmatter `brand:` >
    auto-discovered <repo>/branding/report-brand.json > template defaults.

Dependencies: PyYAML, markdown, weasyprint  (pip install -r requirements.txt).
WeasyPrint needs native libraries (Pango/cairo/GDK-PixBuf). On Windows, render
under WSL or install the GTK runtime; macOS: `brew install weasyprint`; Linux:
the distro libpango/libcairo packages.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dep: PyYAML. Install with:  pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    import markdown as md
except ImportError:
    print("Missing dep: markdown. Install with:  pip install markdown", file=sys.stderr)
    sys.exit(2)

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Missing dep: weasyprint. Install with:  pip install weasyprint "
          "(also needs native Pango/cairo libs — see this file's header).", file=sys.stderr)
    sys.exit(2)


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SCRIPT_DIR / "template.html"
DEFAULT_BRAND = REPO_ROOT / "branding" / "report-brand.json"

KIND_LABELS = {
    "report":     "Report",
    "audit":      "Audit Report",
    "plan":       "Architectural Plan",
    "reference":  "Reference",
    "memo":       "Memo",
    "rfc":        "RFC",
    "agent-spec": "Agent Execution Spec",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Maps a brand JSON `colors` key onto the template's --brand-* CSS variable.
_BRAND_COLOR_VARS = {
    "indigo":        "--brand-indigo",
    "violet":        "--brand-violet",
    "violet_soft":   "--brand-violet-soft",
    "accent_light":  "--brand-accent-light",
    "cover_1":       "--brand-cover-1",
    "cover_2":       "--brand-cover-2",
    "cover_3":       "--brand-cover-3",
    "glow_violet":   "--brand-glow-violet",
    "glow_indigo":   "--brand-glow-indigo",
    "mark_from":     "--brand-mark-from",
    "mark_to":       "--brand-mark-to",
    "mark_shadow":   "--brand-mark-shadow",
    "accent_border": "--brand-accent-border",
}


def split_frontmatter(raw: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw
    meta = yaml.safe_load(match.group(1)) or {}
    body = raw[match.end():]
    return meta, body


def first_h1(body: str) -> str | None:
    m = re.search(r"^\s*#\s+(.+?)\s*$", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def render_markdown(body: str) -> str:
    extensions = [
        "extra",           # tables, fenced code, def lists, etc.
        "sane_lists",
        "toc",
        "admonition",
        "attr_list",
        "md_in_html",
        "codehilite",
    ]
    ext_configs = {
        "codehilite": {"guess_lang": False, "css_class": "codehilite", "noclasses": False},
        "toc": {"permalink": False},
    }
    return md.markdown(body, extensions=extensions, extension_configs=ext_configs, output_format="html5")


def substitute(template: str, vars: dict) -> str:
    for key, val in vars.items():
        template = template.replace("{{" + key + "}}", val)
    return template


def html_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def load_branding(meta: dict, brand_arg: Path | None, md_path: Path) -> dict | None:
    """Resolve the active brand, or None to use the template's built-in defaults.

    Precedence: --brand flag > frontmatter `brand:` > auto-discovered
    <repo>/branding/report-brand.json. Any missing-file / parse error degrades to
    None so a render never fails because of branding.
    """
    candidates: list[Path] = []
    if brand_arg:
        candidates.append(Path(brand_arg))
    fm_brand = meta.get("brand")
    if fm_brand:
        p = Path(str(fm_brand))
        candidates.append(p if p.is_absolute() else md_path.parent / p)
    candidates.append(DEFAULT_BRAND)
    for c in candidates:
        try:
            if c.is_file():
                data = json.loads(c.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
        except Exception:
            continue
    return None


def brand_override_style(branding: dict | None) -> str:
    """A <style> block overriding the template's --brand-* defaults, or '' when none."""
    if not branding:
        return ""
    colors = branding.get("colors") or {}
    decls = [f"{var}:{colors[key]};" for key, var in _BRAND_COLOR_VARS.items()
             if isinstance(colors.get(key), str) and colors.get(key).strip()]
    return "<style>:root{" + "".join(decls) + "}</style>" if decls else ""


def build_vars(meta: dict, body_html: str, body_md: str, md_path: Path,
               branding: dict | None = None) -> dict:
    today = dt.date.today().isoformat()
    kind = str(meta.get("kind", "report")).lower()
    title = meta.get("title") or first_h1(body_md) or md_path.stem.replace("-", " ").replace("_", " ").title()
    b = branding or {}
    return {
        "TITLE": html_escape(str(title)),
        "SUBTITLE": html_escape(str(meta.get("subtitle", ""))),
        "KIND_LABEL": html_escape(KIND_LABELS.get(kind, kind.title())),
        "STATUS": html_escape(str(meta.get("status", "draft")).title()),
        "DATE": html_escape(str(meta.get("date", today))),
        "AUTHOR": html_escape(str(meta.get("author", ""))),
        "APP": html_escape(str(meta.get("app", "General"))),
        "ORG": html_escape(str(meta.get("org", b.get("name", "Your Brand")))),
        "ORG_TLD": html_escape(str(meta.get("org_tld", b.get("org_tld", "example.com")))),
        "MARK": html_escape(str(meta.get("mark", b.get("mark", "R")))),
        "BODY": body_html,
    }


def render(md_path: Path, out_path: Path | None = None,
           brand_arg: Path | None = None, template_path: Path | None = None) -> Path:
    template_file = template_path or DEFAULT_TEMPLATE
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found at {template_file}")
    if not md_path.exists():
        raise FileNotFoundError(f"Source not found: {md_path}")

    raw = md_path.read_text(encoding="utf-8")
    meta, body_md = split_frontmatter(raw)
    branding = load_branding(meta, brand_arg, md_path)

    # Strip a leading H1 that duplicates the cover title.
    body_md_for_html = re.sub(r"^\s*#\s+.+?\s*\n", "", body_md, count=1)

    body_html = render_markdown(body_md_for_html)
    template = template_file.read_text(encoding="utf-8")
    vars = build_vars(meta, body_html, body_md, md_path, branding)
    html = substitute(template, vars)

    # Inject the per-document brand override (no-op when using template defaults).
    override = brand_override_style(branding)
    if override:
        html = html.replace("</head>", override + "</head>", 1) if "</head>" in html else override + html

    out = out_path or md_path.with_suffix(".pdf")
    HTML(string=html, base_url=str(md_path.parent)).write_pdf(str(out))
    return out


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Render a Markdown doc to a branded PDF.")
    p.add_argument("source", type=Path,
                   help="Path to the .md file (or a folder; all .md files inside are rendered).")
    p.add_argument("--out", type=Path, default=None,
                   help="Output .pdf path (default: source with .pdf). Ignored for a folder.")
    p.add_argument("--brand", type=Path, default=None,
                   help="Path to a brand JSON (default: auto-discover branding/report-brand.json).")
    p.add_argument("--template", type=Path, default=None,
                   help="Path to an HTML template (default: bundled renderer/template.html).")
    args = p.parse_args(argv)

    src: Path = args.source
    if src.is_dir():
        targets = sorted(src.glob("*.md"))
        if not targets:
            print(f"No .md files found in {src}", file=sys.stderr)
            return 1
        for t in targets:
            out = render(t, brand_arg=args.brand, template_path=args.template)
            print(f"Rendered -> {out}")
        return 0

    out = render(src, args.out, args.brand, args.template)
    print(f"Rendered -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
