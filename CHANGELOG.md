# Changelog

All notable changes to Branded Report are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] — 2026-06-21

First public release.

### Added
- Markdown → PDF renderer (`render-doc-pdf.py`) with a dark **title-page cover**,
  accent headings, severity-friendly tables, callouts, code blocks and a
  kind-label + page-number footer.
- **Brandable theme** via `report-brand.json` — 13 colour tokens plus badge letter
  and org name, mapped onto the template's `--brand-*` CSS variables. Brand
  resolution: `--brand` flag → frontmatter `brand:` → auto-discovered default →
  template defaults, with safe fallback on any error.
- Bundled brands: default (violet), `acme-capital` (pink/blue), `forest` (emerald).
- Drop-in **Claude Code skill** (`branded-report/`) with `SKILL.md` and three
  references: the exact design system, the branding guide, and a recommended
  report structure with a `CRITICAL/HIGH/MEDIUM/LOW/PASS` severity vocabulary.
- Standalone CLI with `--out`, `--brand`, `--template`, and folder rendering.
- Example report, JSON Schema for brand files, and GitHub banner / logo / cover
  preview assets.
