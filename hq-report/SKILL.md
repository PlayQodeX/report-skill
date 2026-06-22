---
name: hq-report
description: >-
  Turn a Markdown file into a polished, branded PDF report — audit, plan, report,
  review, reference, memo, RFC, or agent-spec — with a dark cover / title page,
  accent-coloured headings, severity-friendly tables and a running footer. Use
  whenever asked to create, write, structure, or render a report/audit/plan as a
  PDF, to produce a professional document with a title page from Markdown, or to
  theme a report to a brand. Colours, the logo badge and the org name are set in a
  small JSON file, so the same engine themes any brand without touching the
  template.
---

# HQ Report

Produce a professional PDF from Markdown: a **dark cover / title page**, accent
headings, clean tables, callouts, and a kind-label + page-number footer. The look
is fixed by a template; the **brand** (colours, logo badge letter, org name) is a
small JSON file you can swap per project. Default theme is a violet identity.

A report is **two files**: a hand-edited `.md` (with YAML frontmatter) and the
`.pdf` rendered from it. You never style a document by hand — the cover, colours
and layout live in the renderer.

> Paths below are relative to this skill folder (`hq-report/`).

---

## When to use

Any document you would hand to a stakeholder, client, or auditor: security or code
audits, technical or business reports, architecture plans, references, memos, RFCs.
If it wants a title page and a consistent brand, use this skill.

## Quick start

```bash
# 1) one-time: install the renderer's dependencies
pip install -r renderer/requirements.txt

# 2) write a report.md with frontmatter (schema below), then render it
python3 renderer/render-doc-pdf.py path/to/report.md
# -> writes path/to/report.pdf with the branded cover as page 1
```

Theme it by editing `branding/report-brand.json`, or pass another brand:

```bash
python3 renderer/render-doc-pdf.py report.md --brand branding/examples/acme-capital.json
```

## Frontmatter (YAML)

```yaml
---
title: Quarterly Security Review            # shown big on the cover
subtitle: 12 findings — 1 critical, 3 high, 5 medium, 3 low
kind: audit                                 # report|audit|plan|reference|memo|rfc|agent-spec
status: final                               # draft|final|review|archived
date: 2026-06-21                            # ISO date
author: Jane Doe
app: Payments API                           # the subject — cover "Application" field
---
```

Optional keys: `org`, `org_tld`, `mark` (cover badge letter), `brand` (path to a
brand JSON for this one document). `kind` sets the cover's eyebrow label and the
footer. All keys are optional — sensible defaults fill anything you omit.

## Title page (cover) — page 1

The renderer generates the cover automatically from the frontmatter; never build it
by hand. It is a full-bleed dark page with:

- a **logo badge** (the `mark` letter) + org name and TLD, top-left;
- the **kind label** eyebrow (e.g. `AUDIT REPORT`) in spaced mono caps;
- the **title** (wrap one word in `<span class="accent-word">` to tint it);
- the **subtitle**;
- a bottom metadata strip — `DATE · APPLICATION · STATUS · AUTHOR`.

Body pages then carry a `KIND-LABEL · ORG` / `page / pages` footer. Exact geometry,
colours and sizes are in `references/design-system.md`.

## Branding (per project)

Colours, the badge letter and the org name are **data**, not template edits — they
live in `branding/report-brand.json` (13 colour tokens + `name`/`mark`/`org_tld`).
Resolution precedence: `--brand <file>` → frontmatter `brand:` → auto-discovered
`branding/report-brand.json` → template defaults. To re-skin, copy the file and
change the values; structure and layout never move. Full schema, the variable map
and worked examples in `references/branding.md`.

## Writing a strong report

`references/report-structure.md` describes the recommended structure for audits and
technical reports: numbered sections, a `CRITICAL / HIGH / MEDIUM / LOW / PASS`
severity vocabulary for findings tables, a risk summary, lettered appendices, and a
calm third-person tone. It is opinionated guidance, not enforced by the renderer.

## Requirements & platform note

Python 3.9+, and the renderer deps in `renderer/requirements.txt` (PyYAML,
markdown, **WeasyPrint**). WeasyPrint needs native libraries (Pango / cairo /
GDK-PixBuf):

- **Linux:** install the distro's `libpango`/`libcairo`/`libgdk-pixbuf` packages.
- **macOS:** `brew install weasyprint`.
- **Windows:** render under WSL or install the GTK runtime — a bare Windows Python
  cannot `import weasyprint`.

Verify a render: `pdfinfo report.pdf` reports `Producer: WeasyPrint …` and page 1 is
the dark cover.

## References

- `references/design-system.md` — the complete visual spec (every colour, font,
  size; the cover/title-page layout; body, tables, callouts, footer). Reproduce the
  look exactly, even by hand.
- `references/branding.md` — the `report-brand.json` schema, the `--brand-*`
  variable map, precedence, and how to re-brand.
- `references/report-structure.md` — recommended report structure, severity
  vocabulary and tone.
