# Website redesign — Astfalck Design System

**Date:** 2026-06-05
**Branch:** `redesign` (main untouched until merged)
**Sources:** `../astfalck-design-system/` (unzipped from "Astfalck Design System.zip")
— `README.md` (voice + visual foundations), `colors_and_type.css` (tokens),
`ui_kits/website/` (target mockup), `fonts/` (Clancy / Roboto / Roboto Mono).

## Goal

Restyle astfalckl.github.io to the Astfalck Design System (Stream palette,
Clancy/Roboto type, single-column text-first layout), and slim the repo and
content while doing it. Keep the Quarto workflow: edit `.qmd`, `quarto render`,
GitHub Pages serves `docs/`.

## Non-goals

- No change to `main` until the user merges.
- No change to deployed `docs/notes/` or `docs/writing/` output (live URLs keep
  working) — only their *sources* are removed from the branch.
- No re-rendering or restyling of the presentation decks under
  `presentations/*/` — only the listing page that indexes them.
- No new content sections.

## Architecture

Quarto website with a custom SCSS theme. Tokens become Bootstrap variables, so
Quarto chrome inherits the brand instead of being patched over.

### Files

| Path | Change |
|------|--------|
| `theme/astfalck.scss` | New. Single custom theme: token layer (ported from `colors_and_type.css`), Bootstrap variable mapping, component patterns (ported from `ui_kits/website/site.css`). Replaces `theme: sandstone` and the near-empty `styles.css`. |
| `fonts/` | New. Self-hosted subset only: Clancy Light/Regular/Bold (otf); Roboto Light/Regular/Medium/Bold + italics (ttf); Roboto Mono Regular/Medium (ttf). `@font-face` declarations live in the theme. |
| `_quarto.yml` | Theme swap; single-column body width (~720px content); nav unchanged in items (Home / Publications / Software / Presentations); remove commented-out writing nav entry; footer kept (CC-BY-NC line), restyled. |
| `index.qmd` | Rewritten. Drop `about: trestles`. Hand-built hero + About + Selected research + Contact (see Content). |
| `publications.qmd` | Rewritten to the reference-list pattern. |
| `software.qmd` | Rewritten; inline-style/float HTML removed. |
| `presentations.qmd` | Keep Quarto listing; restyle via theme CSS. |
| `styles.css` | Removed (superseded by theme). |
| `writing.qmd`, `writing/` | Removed from branch (archived). |
| `notes/` | Removed from branch (archived). |
| `.gitignore` | Add `.DS_Store`; untrack existing copies. |

### Theme contents (`theme/astfalck.scss`)

1. **Tokens** (`:root` CSS custom properties, verbatim values from
   `colors_and_type.css`): Stream palette — paper `#F8F7F3`, sunk `#EEEBE3`,
   ink `#211C16`/`#4A4239`/`#8A8073`, hairline `rgba(33,28,22,.12)`, sage
   `#5A7468`/`#41564C`, terracotta `#9D5242`, yellow `#FFDC00` (marker
   highlight only); 4px spacing scale; radii 2/4/8px; soft warm shadows;
   motion 200ms `cubic-bezier(.2,0,.1,1)`.
2. **Bootstrap/Quarto variables**: `$body-bg` paper, `$body-color` ink,
   `$link-color` sage-deep with terracotta hover, `$font-family-base` Roboto,
   `$headings-font-family` Clancy, `$font-family-monospace` Roboto Mono,
   `$navbar-bg` translucent paper.
3. **Components** (from the UI kit):
   - Sticky header: blurred paper scrim, Clancy wordmark, text nav with
     2px terracotta underline on the active item.
   - Section-head motif: mono UPPERCASE terracotta kicker → Clancy heading
     (sentence case) → 40px × 2px ink rule.
   - `.reflist` / `.ref`: year gutter (mono, faint), hanging indent, author
     name in ink at medium weight, venue italic, mono links.
   - `.pkg` rows and listing items: hairline dividers, no cards.
   - `.ftlink`: small inline-SVG icon links (no icon CDN).
   - Yellow `.mark` marker-highlight utility (used at most once).
   - `prefers-reduced-motion` respected.

## Content

Voice rules from the design README apply: sentence case headings, Australian
spelling, no emoji, plain and short. Mockup edits adopted at Claude's
discretion; all facts, links, and the full publication list come from the
current site.

- **Home**: kicker `LECTURER IN STATISTICS · UNSW SYDNEY`; name in Clancy;
  role line "Spatial & spectral statistics, uncertainty quantification — and a
  lot of applied work in *water*."; social links GitHub / Scholar / Email / CV
  (real URLs from current `index.qmd`); headshot right (4px radius). About
  prose lightly tightened per the mockup, both background paragraphs kept.
  Selected research as a reference list (the current five entries). Contact
  paragraph kept verbatim.
- **Publications**: grouped In review / 2025 / 2024 / 2023 / 2022 and earlier;
  every entry from the current page with its link; typography cleanup
  (stray `''`/`'` quotes, `&` vs `and` consistency, em-dash usage).
- **Software**: bskernel, speccy, bayeslinear, dwelch, gptide — current
  descriptions lightly tidied; hex logos kept, inset small (~96px) on the
  right of each row.
- **Presentations**: listing unchanged in mechanism; CSS restyles it to the
  quiet talks-list look with small right-aligned thumbnails.

## Slimming

- Archive first: `cp -R notes writing ~/Documents/Admin/website_archive/`,
  then `git rm -r` on the branch. History retains them regardless.
- `.DS_Store` ignored and untracked.
- `docs/` re-rendered by Quarto; `docs/notes/` and `docs/writing*` left in
  place (Quarto does not delete unknown output files).

## Verification

1. `quarto render` completes clean.
2. Open rendered pages locally; visually compare each of the four pages
   against `ui_kits/website/index.html` mockup.
3. Confirm `docs/notes/index.html` still exists after render.
4. Confirm CV PDF, headshot, software images resolve.
5. Mobile-width check (hero stacks, nav wraps) at ~600px.

## Risks

- **Clancy licence**: Clancy is UNSW's licensed Monotype face. Self-hosting on
  a public site is assumed acceptable for UNSW staff use; if not, the theme
  falls back gracefully (font stack: Clancy → Roboto → system).
- **Bootstrap specificity**: Quarto's defaults may need targeted overrides;
  kept in one theme file rather than patch layers.
- **Listing markup**: Quarto's listing HTML is version-dependent; styling
  targets its stable classes (`.quarto-post` etc.).
