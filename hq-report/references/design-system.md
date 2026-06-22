# Design system — exact visual spec

The complete specification of the report look, transcribed from `renderer/
template.html`. The template + `renderer/render-doc-pdf.py` are the executable
source of truth; this file mirrors them so the look can be reproduced or audited by
hand. **Brand colours, the badge letter and the org name are overridable** (see
`branding.md`); every other value is fixed structure — don't override it per
document.

Page size **A4**. Fonts: **Inter** (sans) for everything, **JetBrains Mono** (with
`SF Mono`, `Fira Code`, `Courier New` fallbacks) for code, eyebrows, labels and
page numbers. Bring your own font files if you want the exact faces; otherwise the
system fallbacks apply.

---

## Palette

Ink scale (neutrals, fixed):

| Token | Hex | Token | Hex |
|-------|-----|-------|-----|
| `--ink-900` | `#0B0E14` | `--ink-400` | `#6B7388` |
| `--ink-800` | `#141821` | `--ink-300` | `#9EA6BC` |
| `--ink-700` | `#1E2230` | `--ink-200` | `#C9CFDE` |
| `--ink-600` | `#2A2F40` | `--ink-100` | `#E8EBF2` |
| `--ink-500` | `#4A5068` | `--paper`   | `#FAFBFC` |

Brand + semantic (the brand row is overridable via a brand JSON):

| Token | Default | Role |
|-------|---------|------|
| `--indigo` | `#6366F1` | brand secondary (badge gradient start) |
| `--violet` | `#8B5CF6` | **`--accent`** — headings, rules, links, markers |
| `--violet-soft` | `#F5F3FF` | **`--accent-soft`** — table header / blockquote bg |
| `--indigo-soft` | `#EEF0FF` | (reserved) |
| cover accent word | `#C4B5FD` | light tint on a single title word |
| `--emerald` / soft | `#10B981` / `#ECFDF5` | callout `ok` |
| `--amber` / soft | `#F59E0B` / `#FEF3C7` | callout `note` |
| `--rose` / soft | `#F43F5E` / `#FEE2E2` | callout `warn` |
| `--sky` / soft | `#0EA5E9` / `#F0F9FF` | callout `info` |

`--accent: var(--violet)` and `--accent-soft: var(--violet-soft)` — re-skinning the
brand recolours every accent surface at once.

---

## Page geometry & footer

- `@page` A4, margin **18mm 16mm 22mm 16mm**.
- Footer **bottom-left**: `«KIND_LABEL» · «ORG»` — Inter 8pt, `--ink-300`,
  letter-spacing 0.08em, uppercase.
- Footer **bottom-right**: `counter(page) " / " counter(pages)` — JetBrains Mono
  8pt, `--ink-400`.
- `@page :first` (the cover): margin 0, **no footer**.
- Body root: Inter, `--ink-900` on `--paper`, **10.5pt**, line-height **1.6**,
  letter-spacing −0.003em. Content column `max-width: 165mm`.

---

## Title page (cover) — page 1

Full-bleed dark page, `height: 297mm`, `padding: 38mm 20mm 22mm 20mm`, flex column
`justify-content: space-between`.

**Background** (layered, in order):

```css
background:
  radial-gradient(circle at 75% 10%, var(--brand-glow-violet) 0%, transparent 55%),  /* glow, top-right */
  radial-gradient(circle at 10% 85%, var(--brand-glow-indigo) 0%, transparent 55%),  /* glow, bottom-left */
  linear-gradient(135deg, var(--brand-cover-1) 0%, var(--brand-cover-2) 40%, var(--brand-cover-3) 100%);
```

**Brand lockup** (top-left, gap 10pt):
- Badge: 40pt × 40pt, radius 10pt,
  `linear-gradient(135deg, var(--brand-mark-from) 0%, var(--brand-mark-to) 100%)`,
  white badge letter (`mark`) at 18pt weight 800, letter-spacing −0.04em,
  `box-shadow: 0 8px 28px var(--brand-mark-shadow)`.
- Text: org name (`ORG`) 13pt weight 600 white; under it a `<small>` with the TLD
  (`ORG_TLD`) at 8pt, `rgba(255,255,255,0.5)`, letter-spacing 0.15em, uppercase.

**Title block:**
- Kind eyebrow: JetBrains Mono 9pt, letter-spacing 0.3em, uppercase,
  `rgba(255,255,255,0.55)`.
- Title: **46pt** weight 700, line-height 1.02, letter-spacing −0.03em, white.
  Wrap one word in `<span class="accent-word">` to tint it `var(--brand-accent-light)`.
- Subtitle: 14pt weight 400, `rgba(255,255,255,0.78)`, max-width 420pt,
  line-height 1.5.

**Metadata strip** (bottom): top border `1px rgba(255,255,255,0.1)`, padding-top
20pt, flex gap 36pt. Four items — **Date · Application · Status · Author**:
- label: JetBrains Mono 7.5pt, letter-spacing 0.22em, uppercase,
  `rgba(255,255,255,0.4)`.
- value: 10.5pt weight 500, `rgba(255,255,255,0.92)`.

The cover ends with `page-break-after: always`, so body content starts on page 2.

---

## Body typography

| Element | Spec |
|---------|------|
| `h1` | 22pt / 700, color `--accent`, `border-bottom: 2px solid --accent`, padding-bottom 8pt, margin `26pt 0 10pt` (first-child margin-top 0) |
| `h2` | 16pt / 700, `--ink-900`, with a `::before` tab — 3pt × 13pt `--accent` block, radius 1pt, margin-right 8pt |
| `h3` | 12.5pt / 700, `--ink-800` |
| `h4` | 11pt / 700, `--ink-700`, uppercase, letter-spacing 0.05em |
| `p` | margin `0 0 9pt` |
| `a` | color `--accent`, no underline, `border-bottom: 1px solid var(--brand-accent-border)` |
| `strong` | `--ink-900` / 600 · `em` | `--ink-700` |
| `ul,ol` | margin `4pt 0 10pt`, padding-left 20pt; `li` margin-bottom 3pt; markers `--accent` |
| `hr` | `border-top: 1px solid --ink-100`, margin `18pt 0` |

## Code

- Inline `code`: JetBrains Mono 9pt, bg `--ink-100` (`#E8EBF2`), color `--ink-800`,
  padding 1pt 4pt, radius 3pt.
- Block `pre`: JetBrains Mono 8.8pt, line-height 1.55, bg `--ink-900` (`#0B0E14`),
  color `#E8EBF2`, padding 10pt 12pt, radius 6pt, `border-left: 3pt solid --accent`,
  `page-break-inside: avoid`. `pre code` resets bg/padding.

## Tables

- `table`: 100% width, border-collapse, 9.5pt.
- `thead th`: bg `--accent-soft`, `--ink-900`, weight 600, text-align left, padding
  7pt 9pt, `border-bottom: 1.5px solid --accent`, 9pt, letter-spacing 0.02em.
- `tbody td`: padding 6pt 9pt, `border-bottom: 1px solid --ink-100`, vertical-align
  top.
- `tbody tr:nth-child(even) td`: bg `#FBFCFD` (zebra).

## Blockquote & callouts

- `blockquote`: margin `10pt 0 12pt`, padding 10pt 14pt, `border-left: 3pt solid
  --accent`, bg `--accent-soft`, color `--ink-800`, radius `0 4pt 4pt 0`.
- Manual `.callout` boxes (radius 5pt, `border-left: 3pt solid`):
  - `.warn` — bg `--rose-soft`, border `--rose`, text `#7F1D1D`.
  - `.info` — bg `--sky-soft`, border `--sky`, text `#0C4A6E`.
  - `.ok` — bg `--emerald-soft`, border `--emerald`, text `#064E3B`.
  - `.note` — bg `--amber-soft`, border `--amber`, text `#78350F`.
- Markdown `> [!NOTE]` / `> [!WARNING]` render as bold-labelled blockquotes.

## Other

- `.doc-meta` banner: flex gap 20pt, padding 8pt 12pt, bg `--ink-100`, radius 5pt,
  JetBrains Mono 8.5pt, `--ink-600`.
- Task lists: `ul.task-list` unstyled markers; `input[type=checkbox]`
  `accent-color: --accent`.

---

## How brand tokens reach the page

The template's `:root` defines 13 `--brand-*` variables with the default values
above; the renderer injects a `<style>:root{…}</style>` override carrying only the
keys a brand JSON supplies. Accent surfaces resolve through `--accent → --violet →
--brand-violet`, so changing one token recolours everything that uses it. The badge
letter and org name fill the `{{MARK}}` / `{{ORG}}` / `{{ORG_TLD}}` cover
placeholders. Full mapping in `branding.md`.
