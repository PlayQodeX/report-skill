# Branding — theme any project

The report **structure and layout are fixed**; only the **brand** is swappable, and
the brand is data — a small JSON file, not template edits.

- **Default file:** `branding/report-brand.json` (auto-discovered by the renderer).
- **Schema:** `branding/report-brand.schema.json` (field reference + validation).
- **Examples:** `branding/examples/*.json`.
- **What's brandable:** the badge letter, the org name + TLD, and 13 colour tokens
  that drive the cover and every accent surface. Everything else (ink scale, fonts,
  sizes, spacing, semantic callout colours) is structure and never changes.

---

## Schema

```jsonc
{
  "name": "Your Brand",       // cover org name + footer (frontmatter `org` overrides)
  "mark": "R",                // single character in the cover logo badge
  "org_tld": "example.com",   // small caps line under the org name
  "colors": {
    "indigo":        "#6366F1",                  // badge gradient start + brand secondary
    "violet":        "#8B5CF6",                  // --accent: headings, rules, links, markers
    "violet_soft":   "#F5F3FF",                  // --accent-soft: table header / blockquote bg
    "accent_light":  "#C4B5FD",                  // tinted title word on the cover
    "cover_1":       "#0B0E14",                  // cover gradient — darkest stop
    "cover_2":       "#14121F",                  // cover gradient — mid stop
    "cover_3":       "#1E2230",                  // cover gradient — lightest stop
    "glow_violet":   "rgba(139, 92, 246, 0.35)", // cover glow, top-right
    "glow_indigo":   "rgba(99, 102, 241, 0.28)", // cover glow, bottom-left
    "mark_from":     "#6366F1",                  // badge gradient start
    "mark_to":       "#8B5CF6",                  // badge gradient end
    "mark_shadow":   "rgba(139, 92, 246, 0.45)", // badge drop shadow
    "accent_border": "rgba(139, 92, 246, 0.3)"   // inline-link underline
  }
}
```

Every `colors` key is optional — omit one and it falls back to the template default,
so a brand can override just `violet` + `mark` if that's all it needs. Values are
any valid CSS colour; use `rgba()` where transparency matters (the cover glows and
the link underline).

## How it's applied

1. **Resolve** the active brand by precedence: `--brand <path>` →
   frontmatter `brand: <path>` → auto-discovered `branding/report-brand.json` →
   none (template defaults). Any missing-file / parse error degrades to *none* —
   branding never breaks a render.
2. **`colors.<key>` → `--brand-<key>` CSS variable.** The template's `:root`
   defines each `--brand-*` default; the renderer injects a `<style>:root{…}</style>`
   override before `</head>` with only the keys the brand supplies. Because accent
   surfaces resolve through `--accent → --violet → --brand-violet`, recolouring one
   token recolours every surface that uses it.
3. **`mark` / `name` / `org_tld`** fill the `{{MARK}}` / `{{ORG}}` / `{{ORG_TLD}}`
   cover placeholders (frontmatter `org` / `org_tld` / `mark` win if both are set).

## Usage

```bash
# default brand (branding/report-brand.json)
python3 renderer/render-doc-pdf.py report.md

# a specific brand
python3 renderer/render-doc-pdf.py report.md --brand branding/examples/acme-capital.json
```

Per document, in frontmatter:

```yaml
brand: ./brand/acme.json    # relative to the .md file
```

## Re-branding

1. Copy `branding/report-brand.json` (or one of the examples) to a new file.
2. Change `name`, `mark`, `org_tld`, and the `colors` you want. A minimal re-skin is
   often just `name`, `mark`, `violet`, `indigo`, and the three `cover_*` stops.
3. Render with `--brand <that file>` — or replace `branding/report-brand.json` to
   make it the default for every report.

## Bundled examples

| File | Identity |
|------|----------|
| `branding/report-brand.json` | Default — violet on near-black |
| `branding/examples/acme-capital.json` | Pink/blue on deep navy |
| `branding/examples/forest.json` | Emerald on near-black |

Each renders the identical layout with a different accent, cover gradient, badge and
lockup — proof that one template carries any number of brands.
