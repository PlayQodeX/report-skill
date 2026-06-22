# Report structure & tone

Recommended structure for audits and technical reports. This is **opinionated
guidance, not enforced by the renderer** — any Markdown renders. But a report that
follows it reads like a professional audit, and the design system was built to make
this shape look good.

---

## Frontmatter

```yaml
---
title: <Document title>                    # appears big on the cover
subtitle: <one sentence, often with finding counts>
kind: audit                                # report|audit|plan|reference|memo|rfc|agent-spec
status: final                              # draft|final|review|archived
date: 2026-06-21                           # ISO date
author: <name>
app: <subject / product>                   # cover "Application" field
---
```

`kind` sets the cover eyebrow and footer label. Optional: `org`, `org_tld`, `mark`,
`brand` (see `branding.md`).

## Body structure (audit / technical report)

1. **Numbered top-level sections** — `## 1. Executive Summary`, `## 2. Scope and
   Approach`, `## 3. <topic>`, …
2. **Numbered subsections** — `### 3.1 <subsection>`.
3. **Findings tables with explicit severity.** A clean four-column shape:

   ```
   | Severity | Finding | Location | Action Required |
   ```

   Severity is one of **CRITICAL / HIGH / MEDIUM / LOW / PASS**, bolded:
   - **CRITICAL** — correctness / security / data-integrity defect.
   - **HIGH** — blocks a milestone or a user.
   - **MEDIUM** — quality or operational hygiene.
   - **LOW** — cosmetic or future-facing.
   - **PASS** — explicit confirmation an area was reviewed and is sound.
4. **Risk Summary** — table `| # | Residual item / Risk | Impact | Likelihood | Type |`.
5. **Priority Action Plan / Recommendations** — grouped by horizon (Immediate /
   Short-term / Medium-term) or by area; name ownership and the unblocking outcome.
6. **Conclusion** — restate the standing position in plain language.
7. **Appendices** — **lettered** (`## Appendix A`, `## Appendix B`): cumulative
   finding lists, file references, identifiers.
8. **`---` separators** between major sections.

Other kinds (`plan`, `report`, `reference`, `memo`, `rfc`) reuse the same
numbered-section + table + appendix grammar and drop what doesn't apply.

## Tone

- Long-form prose. Bold the headline finding in the executive summary. Lead with a
  numeric summary: `Total findings: N. Critical: 0 | High: 4 | Medium: 8 | Low: 6.
  Overall score: X / 10.`
- **Audit voice** — third person, calm, specific. No first person ("I found"), no
  jokes, no emoji.
- Cite **file paths / line numbers / locations** in findings so action is
  unambiguous.

## Callouts

Use blockquotes for emphasis, or the manual callout classes:

```html
<div class="callout warn">Critical risk — act before deploy.</div>
<div class="callout info">Context the reader needs.</div>
<div class="callout ok">Verified good.</div>
<div class="callout note">A caveat to keep in mind.</div>
```

(`md_in_html` is enabled, so raw HTML blocks work inside Markdown.)

## Optional: a two-audience pair

A useful pattern for handoffs — ship the same subject twice:

- **Management** `<topic>-<kind>-YYYY-MM-DD.md` — the prose format above; audience is
  a stakeholder.
- **Agent** `<topic>-<kind>-YYYY-MM-DD.agent.md` (`kind: agent-spec`) —
  instruction-grade, no narrative: a short *Context* block, then numbered concrete
  steps (exact paths, commands), each ending in an acceptance check, closing with a
  *Done when* checklist.

Cross-link them in frontmatter (`agent_doc:` / `management_doc:`). Both render with
the same command; the `agent-spec` kind gets its own cover label.
