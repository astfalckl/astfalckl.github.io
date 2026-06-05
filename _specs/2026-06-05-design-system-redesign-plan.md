# Astfalck Design System Website Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle astfalckl.github.io (Quarto site in `/Users/z3550428/Documents/Admin/_website/`) to the Astfalck Design System and slim the repo, on branch `redesign`.

**Architecture:** Custom Quarto SCSS theme (`astfalck.scss`) where design tokens become Bootstrap variables; self-hosted fonts via a root `fonts.css`; qmd content rewritten to the design's text-first patterns. Spec: `_specs/2026-06-05-design-system-redesign-design.md`. Design sources: `../astfalck-design-system/`.

**Tech Stack:** Quarto 1.9.29 website, SCSS, GitHub Pages from `docs/` on main.

**Conventions:** Working dir is `/Users/z3550428/Documents/Admin/_website` on branch `redesign`. This is a static site — "tests" are renders plus grep/file checks with expected output. Do not touch `docs/notes/` or `docs/writing*`. Don't `git add -A`; add explicit paths (the render dirties `docs/` before its commit task).

---

### Task 1: Archive notes/ + writing/, slim the repo

**Files:**
- Create: `~/Documents/Admin/website_archive/` (outside repo)
- Modify: `.gitignore`
- Delete (from branch): `notes/`, `writing/`, `writing.qmd`, tracked `.DS_Store`, unused `images/software/*`

- [ ] **Step 1: Archive the sources outside the repo**

```bash
mkdir -p ~/Documents/Admin/website_archive
cp -R notes ~/Documents/Admin/website_archive/notes
cp -R writing ~/Documents/Admin/website_archive/writing
cp writing.qmd ~/Documents/Admin/website_archive/writing.qmd
```

- [ ] **Step 2: Verify the archive is a faithful copy**

Run: `diff -rq notes ~/Documents/Admin/website_archive/notes && diff -rq writing ~/Documents/Admin/website_archive/writing && echo ARCHIVE-OK`
Expected: `ARCHIVE-OK` (no diff lines).

- [ ] **Step 3: Remove sources from the branch**

```bash
git rm -r -q notes writing writing.qmd
```

(If `git rm` complains about untracked files inside `notes/`, rerun the failing path with `git rm -r -q --force` — the archive copy in Step 1 already preserved everything, and untracked leftovers can be removed with `rm -rf notes writing` afterwards.)

- [ ] **Step 4: Ignore and untrack .DS_Store**

Overwrite `.gitignore` with:

```
/.quarto/

**/*.quarto_ipynb
.DS_Store
**/.DS_Store
```

Then:

```bash
git ls-files | grep '\.DS_Store$' | xargs git rm -q --cached
```

- [ ] **Step 5: Remove unused software images**

Only `bskernel.png`, `speccy2.png`, `bayeslinear2.png`, `dwelch.png`, `gptide.jpeg` are referenced. Remove the rest:

```bash
git rm -q "images/software/bayeslinear.jpg" "images/software/dwelch.jpg" \
  "images/software/dwelch2.jpg" "images/software/speccy.png"
rm -f images/software/DALL*\ 2025-07-01*.webp
```

(The DALL·E file may be untracked — plain `rm` is fine; if `git rm` is needed use a glob: `git rm -q "images/software/DALL"*`.)

- [ ] **Step 6: Verify repo state**

Run: `git status --short | head -30; ls images/software/`
Expected: deletions staged for notes/, writing/, writing.qmd, .DS_Store files, unused images; `images/software/` lists exactly `bayeslinear2.png bskernel.png dwelch.png gptide.jpeg speccy2.png`.

- [ ] **Step 7: Commit**

```bash
git add .gitignore
git commit -m "Archive notes/ and writing/ sources; untrack .DS_Store and unused images

Sources copied to ~/Documents/Admin/website_archive/. Rendered docs/notes/
and docs/writing* are left in place so live URLs keep working.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Self-host the brand fonts

**Files:**
- Create: `fonts/` (11 font files), `fonts.css`

- [ ] **Step 1: Copy the font subset from the design system**

```bash
mkdir -p fonts
SRC=../astfalck-design-system/fonts
cp "$SRC/Clancy-Light.otf" "$SRC/Clancy-Regular.otf" "$SRC/Clancy-Bold.otf" \
   "$SRC/Roboto-Regular.ttf" "$SRC/Roboto-Italic.ttf" "$SRC/Roboto-Medium.ttf" \
   "$SRC/Roboto-MediumItalic.ttf" "$SRC/Roboto-Bold.ttf" "$SRC/Roboto-BoldItalic.ttf" \
   "$SRC/RobotoMono-Regular.ttf" "$SRC/RobotoMono-Medium.ttf" fonts/
```

- [ ] **Step 2: Verify**

Run: `ls fonts | wc -l && ls fonts`
Expected: `11` and the files listed above.

- [ ] **Step 3: Create `fonts.css`** (at repo root; URLs are relative to the stylesheet, which Quarto copies to the site root, so they resolve from any page depth)

```css
/* Self-hosted UNSW brand fonts — Astfalck Design System. */
@font-face { font-family: "Clancy"; src: url("fonts/Clancy-Light.otf") format("opentype"); font-weight: 300; font-style: normal; font-display: swap; }
@font-face { font-family: "Clancy"; src: url("fonts/Clancy-Regular.otf") format("opentype"); font-weight: 400; font-style: normal; font-display: swap; }
@font-face { font-family: "Clancy"; src: url("fonts/Clancy-Bold.otf") format("opentype"); font-weight: 600 700; font-style: normal; font-display: swap; }
@font-face { font-family: "Roboto"; src: url("fonts/Roboto-Regular.ttf") format("truetype"); font-weight: 400; font-style: normal; font-display: swap; }
@font-face { font-family: "Roboto"; src: url("fonts/Roboto-Italic.ttf") format("truetype"); font-weight: 400; font-style: italic; font-display: swap; }
@font-face { font-family: "Roboto"; src: url("fonts/Roboto-Medium.ttf") format("truetype"); font-weight: 500; font-style: normal; font-display: swap; }
@font-face { font-family: "Roboto"; src: url("fonts/Roboto-MediumItalic.ttf") format("truetype"); font-weight: 500; font-style: italic; font-display: swap; }
@font-face { font-family: "Roboto"; src: url("fonts/Roboto-Bold.ttf") format("truetype"); font-weight: 700; font-style: normal; font-display: swap; }
@font-face { font-family: "Roboto"; src: url("fonts/Roboto-BoldItalic.ttf") format("truetype"); font-weight: 700; font-style: italic; font-display: swap; }
@font-face { font-family: "Roboto Mono"; src: url("fonts/RobotoMono-Regular.ttf") format("truetype"); font-weight: 400; font-style: normal; font-display: swap; }
@font-face { font-family: "Roboto Mono"; src: url("fonts/RobotoMono-Medium.ttf") format("truetype"); font-weight: 500; font-style: normal; font-display: swap; }
```

(Note `font-weight: 600 700` on Clancy Bold: headings use weight 600; this range maps 600 onto the Bold cut instead of synthesising.)

- [ ] **Step 4: Commit**

```bash
git add fonts fonts.css
git commit -m "Self-host Clancy / Roboto / Roboto Mono (used weights only)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Custom theme + project config

**Files:**
- Create: `astfalck.scss`
- Modify: `_quarto.yml`
- Delete: `styles.css` (repo root only — leave `docs/styles.css`, old rendered pages link it)

- [ ] **Step 1: Create `astfalck.scss`** with exactly:

```scss
/*-- scss:defaults --*/

// ============================================================================
// Astfalck Design System — "Stream" palette.
// Tokens from ../astfalck-design-system/colors_and_type.css
// ============================================================================

$paper:           #F8F7F3;
$paper-sunk:      #EEEBE3;
$ink:             #211C16;
$ink-2:           #4A4239;
$ink-3:           #8A8073;
$sage:            #5A7468;
$sage-deep:       #41564C;
$sage-wash:       #E7EAE5;
$terracotta:      #9D5242;
$terracotta-deep: #6B3828;
$yellow:          #FFDC00;

// ---- Bootstrap mapping ----
$body-bg:                $paper;
$body-color:             $ink;
$link-color:             $sage-deep;
$link-decoration:        none;
$link-hover-color:       $terracotta;
$font-family-sans-serif: "Roboto", system-ui, -apple-system, "Segoe UI", sans-serif;
$font-family-monospace:  "Roboto Mono", ui-monospace, "SF Mono", Menlo, monospace;
$headings-font-family:   "Clancy", "Roboto", sans-serif;
$headings-font-weight:   600;
$font-size-root:         18px;
$line-height-base:       1.65;
$code-bg:                $paper-sunk;
$code-color:             $ink;
$border-radius:          4px;
$navbar-bg:              rgba($paper, 0.86);
$navbar-fg:              $ink;
$footer-bg:              $paper;

/*-- scss:rules --*/

:root {
  --paper:      #{$paper};
  --paper-sunk: #{$paper-sunk};
  --ink:        #{$ink};
  --ink-2:      #{$ink-2};
  --ink-3:      #{$ink-3};
  --line:       rgba(33, 28, 22, 0.12);
  --sage:       #{$sage};
  --sage-deep:  #{$sage-deep};
  --sage-wash:  #{$sage-wash};
  --terracotta: #{$terracotta};
  --yellow:     #{$yellow};
  --font-display: "Clancy", "Roboto", sans-serif;
  --font-mono: "Roboto Mono", ui-monospace, "SF Mono", Menlo, monospace;
  --dur: 200ms;
  --ease: cubic-bezier(0.2, 0, 0.1, 1);
}

body {
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

/* ---- Links: sage, terracotta on hover, quiet underline ---- */
main a:not(.ftlink) {
  border-bottom: 1px solid rgba(65, 86, 76, 0.35);
  transition: color var(--dur) var(--ease), border-color var(--dur) var(--ease);
}
main a:not(.ftlink):hover {
  border-bottom-color: rgba(157, 82, 66, 0.6);
}

/* ---- Header / nav: sticky paper scrim, wordmark, terracotta active rule ---- */
.navbar {
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line);
}
.navbar-title {
  font-family: var(--font-display);
  font-size: 21px;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.navbar .nav-link {
  font-size: 15px;
  color: var(--ink-3);
  transition: color var(--dur) var(--ease);
}
.navbar .nav-link:hover { color: var(--ink); }
.navbar .nav-link.active {
  color: var(--ink);
  box-shadow: inset 0 -2px 0 var(--terracotta);
}

/* ---- Headings: Clancy, sentence case, short ink rule (section-head motif) ---- */
h1, h2 { letter-spacing: -0.02em; }
#title-block-header { margin-block-end: 2.2rem; }
#title-block-header .title { font-size: 2.1rem; }
#title-block-header .title::after,
main h2::after {
  content: "";
  display: block;
  width: 40px;
  height: 2px;
  background: var(--ink);
  margin-top: 13px;
}
main h2 {
  border-bottom: none;
  padding-bottom: 0;
  margin-top: 3rem;
}

/* ---- Kicker: mono uppercase terracotta label ---- */
.kicker {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--terracotta);
  margin: 0 0 8px;
}

/* ---- Marker-pen highlight (the yellow whisper — use at most once per page) ---- */
mark, .mark {
  background: linear-gradient(180deg, transparent 58%, var(--yellow) 58%, var(--yellow) 92%, transparent 92%);
  color: inherit;
  padding: 0 0.05em;
}

/* ---- Hero (home) ---- */
.hero {
  display: flex;
  gap: 40px;
  align-items: flex-start;
  justify-content: space-between;
  margin: 24px 0 40px;
}
.hero-text { flex: 1; }
.hero-name {
  font-family: var(--font-display);
  font-size: 46px;
  font-weight: 600;
  line-height: 1.05;
  letter-spacing: -0.02em;
  margin: 6px 0 14px;
}
.hero-role {
  font-size: 20px;
  line-height: 1.45;
  color: var(--ink-2);
  max-width: 30ch;
  margin: 0 0 22px;
}
.hero-social { display: flex; flex-wrap: wrap; gap: 8px 20px; }
.hero-photo {
  flex: none;
  width: 200px;
  height: 240px;
  object-fit: cover;
  border-radius: 4px;
}

/* ---- Icon links (hero social) ---- */
.ftlink {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--ink-2);
  transition: color var(--dur) var(--ease);
}
.ftlink:hover { color: var(--terracotta); }
.ftlink svg { width: 15px; height: 15px; }

/* ---- Reference lists (publications, selected research) ---- */
.pubs h3 {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--terracotta);
  margin: 2.4rem 0 1rem;
}
.pubs p {
  font-size: 15px;
  line-height: 1.58;
  color: var(--ink-2);
  padding-left: 1.1em;
  text-indent: -1.1em;
  max-width: 62ch;
  margin-bottom: 14px;
}
.pubs strong { font-weight: 500; color: var(--ink); }
.pubs em { color: var(--ink); }
.pubs p a {
  font-family: var(--font-mono);
  font-size: 12px;
  white-space: nowrap;
}

/* ---- Software: hairline-divided package rows ---- */
.pkg {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  padding: 24px 0;
  border-bottom: 1px solid var(--line);
}
.pkg:last-child { border-bottom: none; }
.pkg-body { flex: 1; }
.pkg-body h3 {
  font-family: var(--font-mono);
  font-size: 17px;
  font-weight: 500;
  margin: 0 0 6px;
}
.pkg-body p {
  font-size: 15px;
  color: var(--ink-2);
  max-width: 60ch;
  margin: 0;
}
.pkg-logo { flex: none; }
.pkg-logo p { margin: 0; }
.pkg-logo img { width: 96px; border-radius: 4px; }

/* ---- Presentations listing (Quarto .quarto-post markup) ---- */
div.quarto-post {
  border-bottom: 1px solid var(--line);
  padding: 20px 0;
  gap: 24px;
}
div.quarto-post .body h3.listing-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 500;
  margin: 0 0 4px;
}
div.quarto-post .body .listing-subtitle { font-size: 14px; color: var(--ink-2); }
div.quarto-post .metadata {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--ink-3);
}
div.quarto-post .thumbnail img { border-radius: 4px; }

/* ---- Footer ---- */
.nav-footer {
  border-top: 1px solid var(--line);
  font-size: 13px;
  color: var(--ink-3);
}

/* ---- Responsive / motion ---- */
@media (max-width: 640px) {
  .hero { flex-direction: column-reverse; gap: 24px; }
  .hero-name { font-size: 40px; }
}
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; }
}
```

- [ ] **Step 2: Overwrite `_quarto.yml`** with exactly:

```yaml
project:
  type: website
  resources:
    - astfalck_cv.pdf
    - "fonts/"
  output-dir: docs

website:
  title: "Lachlan Astfalck"
  navbar:
    background: light
    foreground: dark
    search: false
    left:
      - text: "Home"
        href: index.qmd
      - text: "Publications"
        href: publications.qmd
      - text: "Software"
        href: software.qmd
      - text: "Presentations"
        href: presentations.qmd
  page-footer:
    left: "© 2026 Lachlan Astfalck. Unless stated otherwise, all text and images licensed CC-BY-NC 4.0."

format:
  html:
    theme: astfalck.scss
    css: fonts.css
    toc: false
    anchor-sections: false
    grid:
      body-width: 720px
```

- [ ] **Step 3: Remove the old stylesheet from the source tree**

```bash
git rm -q styles.css
```

- [ ] **Step 4: Render and verify the theme applies**

Run: `quarto render 2>&1 | tail -5`
Expected: `Output created: docs/index.html` (no errors).

Run: `grep -o 'background-color: #F8F7F3' docs/site_libs/bootstrap/bootstrap*.min.css | head -1; ls docs/fonts/ | wc -l; grep -c 'fonts.css' docs/index.html`
Expected: the hex match prints; `11`; `1` (or more).

- [ ] **Step 5: Commit (source only, not docs)**

```bash
git add astfalck.scss _quarto.yml
git commit -m "Add Astfalck Design System theme; drop sandstone

Stream palette tokens as Bootstrap vars, Clancy/Roboto/Roboto Mono,
single-column 720px layout, section-head motif, reference-list and
package-row patterns.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Rewrite `index.qmd` (hero, about, selected research, contact)

**Files:**
- Modify: `index.qmd` (full overwrite)

- [ ] **Step 1: Overwrite `index.qmd`** with exactly:

````markdown
---
pagetitle: "Lachlan Astfalck"
---

```{=html}
<section class="hero">
  <div class="hero-text">
    <p class="kicker">Lecturer in Statistics · UNSW Sydney</p>
    <h1 class="hero-name">Lachlan Astfalck</h1>
    <p class="hero-role">Spatial and spectral statistics, uncertainty
    quantification — and a lot of applied work in <em>water</em>.</p>
    <div class="hero-social">
      <a class="ftlink" href="https://github.com/astfalckl">
        <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
        GitHub</a>
      <a class="ftlink" href="https://scholar.google.com/citations?user=duQ38MgAAAAJ&hl=en&oi=ao">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/></svg>
        Scholar</a>
      <a class="ftlink" href="mailto:l.astfalck@unsw.edu.au">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
        Email</a>
      <a class="ftlink" href="astfalck_cv.pdf">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>
        CV</a>
    </div>
  </div>
  <img class="hero-photo" src="images/headshot.jpg" alt="Lachlan Astfalck" />
</section>
```

## About

I'm a Lecturer in Statistics at the University of New South Wales, with
interest in both methodological and applied research. On the methods side:
spectral analysis, complex spatio-temporal data, emulation of engineering
computer models, and many aspects of uncertainty quantification. I also like
water — I do lots of applied work in oceanography, glaciology and
hydrodynamics.

Previously I was a Research Fellow for the TIDE ARC ITRH in the School of
Physics, Mathematics and Computing at The University of Western Australia, and
a Research Fellow in the School of Earth and Environment at the University of
Leeds. I've also worked in ecological restoration, materials engineering, and
prognostics and health management, and consulted for the Australian Wildlife
Conservancy.

## Selected research

::: {.pubs}
**LC Astfalck**, AM Sykulski and EJ Cripps (2024). 'Debiasing Welch's Method
for Spectral Density Estimation'. *Biometrika*, 111(4), 1313–1329.
[paper](https://academic.oup.com/biomet/article/111/4/1313/7703280)

**LC Astfalck**, DB Williamson, N Gandy, LJ Gregoire and RF Ivanovic (2024).
'Coexchangeable Process Modeling for Uncertainty Quantification in Joint
Climate Reconstruction'. *Journal of the American Statistical Association*,
119(547), 1751–1764.
[paper](https://www.tandfonline.com/doi/full/10.1080/01621459.2024.2325705)

**LC Astfalck**, AM Sykulski and EJ Cripps (2025). 'Bias Correction of
Quadratic Spectral Estimators'. *Biometrika*, asaf033.
[paper](https://academic.oup.com/biomet/advance-article/doi/10.1093/biomet/asaf033/8121249)

R Ou, **LC Astfalck**, D Sen and DB Dunson (2026). 'Scalable Bayesian
inference for time series via divide-and-conquer'. Accepted (minor revisions),
*Journal of the American Statistical Association*.
[preprint](https://arxiv.org/pdf/2106.11043)

**LC Astfalck**, D Sen, S Patra, EJ Cripps and DB Dunson (2025). 'Posterior
Projection for Inference in Constrained Spaces'. Submitted to the *SIAM/ASA
Journal on Uncertainty Quantification*.
[preprint](https://arxiv.org/abs/1812.05741)
:::

## Contact

Please contact me via email, I very seldom check any social media channels,
including LinkedIn. I am accepting research students in statistics and
oceanography, don't be shy in reaching out.
````

- [ ] **Step 2: Render and verify**

Run: `quarto render index.qmd 2>&1 | tail -3 && grep -c 'hero-name' docs/index.html && grep -c 'quarto-about-trestles' docs/index.html; true`
Expected: `Output created: docs/index.html`; `1` (hero present); `0` (trestles gone).

- [ ] **Step 3: Commit**

```bash
git add index.qmd
git commit -m "Rewrite home page: hero, about, selected research, contact

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Rewrite `publications.qmd` (reference-list pattern)

**Files:**
- Modify: `publications.qmd` (full overwrite)

Formatting rules applied: authors with **LC Astfalck** in bold; consistent
"and" before the final author; titles in plain quotes (case as published);
venue in italics; mono link labels `[paper]` / `[preprint]` / `[pdf]`; all
current entries kept; the Ou et al. JASA paper (currently only on the home
page) added under "In review".

- [ ] **Step 1: Overwrite `publications.qmd`** with exactly:

````markdown
---
title: "Publications"
---

::: {.pubs}

### In review

**LC Astfalck** (2025). 'Universal approximation of auto-covariance functions
via spline kernels'. Submitted to the *Journal of the Royal Statistical
Society: Series B*. [preprint](https://arxiv.org/abs/2506.21953)

R Ou, **LC Astfalck**, D Sen and DB Dunson (2026). 'Scalable Bayesian
inference for time series via divide-and-conquer'. Accepted (minor revisions),
*Journal of the American Statistical Association*.
[preprint](https://arxiv.org/pdf/2106.11043)

**LC Astfalck**, D Sen, S Patra, EJ Cripps and DB Dunson (2025). 'Posterior
Projection for Inference in Constrained Spaces'. Submitted to the *SIAM/ASA
Journal on Uncertainty Quantification*.
[preprint](https://arxiv.org/abs/1812.05741)

T Tang, **LC Astfalck** and DB Dunson (2025). 'Efficient Bayesian Inference
for Discretely Observed Continuous Time Markov Chains'. Submitted to the
*Journal of the American Statistical Association*.
[preprint](https://arxiv.org/abs/2507.16756)

RY Zhang, HB Moss, **LC Astfalck**, EJ Cripps and DS Leslie (2025).
'Spatio-temporal active learning of time-dependent vector fields using
Lagrangian observers'. Submitted to *The Thirty-Ninth Annual Conference on
Neural Information Processing Systems*.

Y Zheng, MD Rayson, **LC Astfalck** and NL Jones (2025). 'A Machine Learning
Parameterization for the Internal Gravity Wave Spectrum'. Submitted to the
*Journal of Geophysical Research: Oceans*.
[preprint](https://d197for5662m48.cloudfront.net/documents/publicationstatus/266065/preprint_pdf/988284777de79f16ee1eccb3e61e2d40.pdf)

**LC Astfalck**, CR Bird and DB Williamson (2024). 'Generalised Bayes Linear
Inference'. Submitted to *Bayesian Analysis*.
[preprint](https://arxiv.org/pdf/2405.14145)

### 2025

**LC Astfalck**, AM Sykulski and EJ Cripps (2025). 'Bias Correction of
Quadratic Spectral Estimators'. *Biometrika*, asaf033.
[paper](https://academic.oup.com/biomet/advance-article/doi/10.1093/biomet/asaf033/8121249)

MD Rayson, **LC Astfalck**, ALS Ponte, AP Zulberti and NL Jones (2025).
'Characteristic velocity and timescales of non-phase-locked internal tides in
a mesoscale eddy field'. *Journal of Geophysical Research: Oceans*, 130(6),
e2024JC021789.
[paper](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JC021789)

IA Milne, **LC Astfalck**, M Zed and J Lee-Kopij (2025). 'Response-Based
Forecasting of Vessel Motion: From Physics-Based to Data-Driven Methods'.
*Offshore Technology Conference*.

### 2024

**LC Astfalck**, AM Sykulski and EJ Cripps (2024). 'Debiasing Welch's Method
for Spectral Density Estimation'. *Biometrika*, 111(4), 1313–1329.
[paper](https://academic.oup.com/biomet/article/111/4/1313/7703280)

**LC Astfalck**, DB Williamson, N Gandy, LJ Gregoire and RF Ivanovic (2024).
'Coexchangeable Process Modeling for Uncertainty Quantification in Joint
Climate Reconstruction'. *Journal of the American Statistical Association*,
119(547), 1751–1764.
[paper](https://www.tandfonline.com/doi/full/10.1080/01621459.2024.2325705)

ALS Ponte, **LC Astfalck**, MD Rayson, AP Zulberti and NL Jones (2024).
'Inferring flow energy, space and time scales: freely-drifting vs fixed point
observations'. *Nonlinear Processes in Geophysics*, 31(4), 571–586.
[paper](https://npg.copernicus.org/articles/31/571/2024/npg-31-571-2024.html)

RY Zhang, HB Moss, **LC Astfalck**, EJ Cripps and DS Leslie (2024). 'BALLAST:
Bayesian Active Learning with Look-ahead Amendment for Sea-drifter
Trajectories'. *NeurIPS 2024 Workshop on Bayesian Decision-making and
Uncertainty*.

IA Milne and **LC Astfalck** (2024). 'Heave response spectra for a
semisubmersible in long period swell'. *24th Australasian Fluid Mechanics
Conference*.

N Gandy, **LC Astfalck**, GL Ives and GE Rivers (2024). 'Ice sheet
speed-dating: using expert judgement to identify "good" simulations of the LGM
North American ice sheets'. *Quaternary Science Reviews*, 333, 108690.
[paper](https://www.sciencedirect.com/science/article/pii/S0277379124001914?dgcid=rss_sd_all)

VL Patterson, LJ Gregoire, RF Ivanovic, N Gandy, J Owen, RS Smith, PJ Valdes,
OG Pollard and **LC Astfalck** (2024). 'Contrasting the Penultimate and Last
Glacial Maxima (21 and 140 ka BP) using coupled climate-ice sheet modelling'.
*Climate of the Past*.
[paper](https://cp.copernicus.org/preprints/cp-2024-10/)

### 2023

**LC Astfalck**, M Bertolacci and EJ Cripps (2023). 'Evaluating probabilistic
forecasts for maritime engineering operations'. *Data-Centric Engineering*,
4, e15.
[paper](https://www.cambridge.org/core/journals/data-centric-engineering/article/evaluating-probabilistic-forecasts-for-maritime-engineering-operations/17A5733A76CEBCFC6A74F5897F7D4D4B)

OG Pollard, NL Barlow, LJ Gregoire, N Gomex, V Cartelle, JC Ely and
**LC Astfalck** (2023). 'Quantifying the uncertainty in the Eurasian ice-sheet
geometry at the Penultimate Glacial Maximum (Marine Isotope Stage 6)'.
*The Cryosphere*, 17(11), 4751–4777.
[paper](https://tc.copernicus.org/articles/17/4751/2023/tc-17-4751-2023.pdf)

N Gandy, **LC Astfalck**, LJ Gregoire, RF Ivanovic and VL Patterson (2023).
'De-tuning a coupled climate ice sheet model to simulate the North American
ice sheet at the Last Glacial Maximum'. *Journal of Geophysical Research:
Earth Surface*, 128(8), e2023JF007250.
[paper](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023JF007250)

### 2022 and earlier — pre-postdoctoral research

MA Loake, **LC Astfalck** and EJ Cripps (2022). 'Modelling sea surface wind
measurements on Australia's North-West Shelf'. *Ocean Engineering*, 244,
110308.
[paper](https://www.sciencedirect.com/science/article/pii/S0029801821016115)

M Masarei, **LC Astfalck**, AL Guzzomi, DJ Merritt and TE Erickson (2020).
'Soil rock content influences the maximum seedling emergence depth of a
dominant arid zone grass'. *Plant and Soil*, 450(1), 497–509.
[paper](https://link.springer.com/article/10.1007/s11104-020-04493-5)

**LC Astfalck**, EJ Cripps, MR Hodkiewicz and IA Milne (2019). 'A Bayesian
approach to the quantification of extremal responses in simulated dynamic
structures'. *Ocean Engineering*, 182, 594–607.
[paper](https://www.sciencedirect.com/science/article/pii/S0029801819301738)

**LC Astfalck**, EJ Cripps, JP Gosling and IA Milne (2019). 'Emulation of
vessel motion simulators for computationally efficient uncertainty
quantification'. *Ocean Engineering*, 172, 726–736.
[paper](https://www.sciencedirect.com/science/article/pii/S0029801818310898)

**LC Astfalck**, EJ Cripps, JP Gosling, MR Hodkiewicz and IA Milne (2018).
'Expert elicitation of directional metocean parameters'. *Ocean Engineering*,
161, 268–276.
[paper](https://www.sciencedirect.com/science/article/pii/S0029801818305353)

**LC Astfalck**, GK Kelly, X Li and TB Sercombe (2017). 'On the breakdown of
SiC during the selective laser melting of aluminum matrix composites'.
*Advanced Engineering Materials*, 19(8), 1600835.
[paper](https://onlinelibrary.wiley.com/doi/full/10.1002/adem.201600835)

**LC Astfalck** and MR Hodkiewicz (2017). 'Hamiltonian Monte Carlo sampling
for Bayesian hierarchical regression in prognostics'. *Asia Pacific Conference
of the Prognostics and Health Management Society*.

**LC Astfalck**, MR Hodkiewicz, A Keating, EJ Cripps and M Pecht (2016). 'A
modelling ecosystem for prognostics'. *Annual Conference of the Prognostics
and Health Management Society*.

J Sikorska, MR Hodkiewicz, A D'Cruz, **LC Astfalck** and A Keating (2016). 'A
collaborative data library for testing prognostic models'. *Prognostics and
Health Management Society European Conference*.

:::
````

- [ ] **Step 2: Render and verify**

Run: `quarto render publications.qmd 2>&1 | tail -3 && grep -c 'class="pubs"' docs/publications.html && grep -o 'href="https://arxiv[^"]*"' docs/publications.html | wc -l`
Expected: `Output created: docs/publications.html`; `1`; `5` (five arXiv links).

- [ ] **Step 3: Commit**

```bash
git add publications.qmd
git commit -m "Rewrite publications as reference list; add Ou et al. JASA entry

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6: Rewrite `software.qmd` (package rows, no inline styles)

**Files:**
- Modify: `software.qmd` (full overwrite)

- [ ] **Step 1: Overwrite `software.qmd`** with exactly:

````markdown
---
title: "Software"
---

::: {.pkg}
::: {.pkg-body}
### [bskernel](https://astfalckl.github.io/bskernel/index.html)

Flexible non-parametric auto-covariance functions via spline kernels, plus
some handy tools for optimisation.
:::
::: {.pkg-logo}
![](images/software/bskernel.png)
:::
:::

::: {.pkg}
::: {.pkg-body}
### [speccy](https://github.com/astfalckl/speccy)

R package for modern spectral analysis. The plan is for this to be a one-stop
shop for spectral analysis in R. Still in development.
:::
::: {.pkg-logo}
![](images/software/speccy2.png)
:::
:::

::: {.pkg}
::: {.pkg-body}
### [bayeslinear](https://github.com/astfalckl/bayeslinear)

R package for Bayes linear analysis: all the old school Bayes linear
mathematics, as well as the recent 'generalised' developments.
:::
::: {.pkg-logo}
![](images/software/bayeslinear2.png)
:::
:::

::: {.pkg}
::: {.pkg-body}
### [dwelch](https://github.com/astfalckl/dwelch)

Companion to 'Debiasing Welch's Method for Spectral Density Estimation'. This
code will eventually be subsumed into
[speccy](https://github.com/astfalckl/speccy).
:::
::: {.pkg-logo}
![](images/software/dwelch.png)
:::
:::

::: {.pkg}
::: {.pkg-body}
### [gptide](https://gptide.readthedocs.io/en/latest/)

A lightweight Gaussian process regression toolkit in Python. There are many
other GP packages — this is yet another one. The selling point: the object is
fairly straightforward, and kernel building is all done with functions, not
abstract classes.
:::
::: {.pkg-logo}
![](images/software/gptide.jpeg)
:::
:::
````

- [ ] **Step 2: Render and verify**

Run: `quarto render software.qmd 2>&1 | tail -3 && grep -c 'class="pkg"' docs/software.html && grep -c 'hspace' docs/software.html; true`
Expected: `Output created: docs/software.html`; `5` (five package rows); `0` (inline-style HTML gone).

- [ ] **Step 3: Commit**

```bash
git add software.qmd
git commit -m "Rewrite software page as hairline package rows

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 7: Tidy `presentations.qmd`

**Files:**
- Modify: `presentations.qmd` (full overwrite)

- [ ] **Step 1: Overwrite `presentations.qmd`** with exactly:

```markdown
---
title: "Presentations"
listing:
  contents: presentations
  type: default
  sort: "date desc"
  image-align: right
  image-height: "120px"
  fields: [image, date, title, subtitle]
---
```

- [ ] **Step 2: Render and verify**

Run: `quarto render presentations.qmd 2>&1 | tail -3 && grep -c 'quarto-post' docs/presentations.html`
Expected: `Output created: docs/presentations.html`; a count ≥ 8 (one per talk).

- [ ] **Step 3: Commit**

```bash
git add presentations.qmd
git commit -m "Tidy presentations listing config

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 8: Full render, site-wide verification, commit docs/

**Files:**
- Modify: `docs/` (rendered output)

- [ ] **Step 1: Clean full render**

```bash
quarto render 2>&1 | tail -5
```

Expected: ends with `Output created: docs/index.html`, no ERROR lines.

- [ ] **Step 2: Verify nondestructive guarantees and resources**

```bash
test -f docs/notes/index.html && echo NOTES-OK
test -f docs/writing.html && echo WRITING-OK
test -f docs/astfalck_cv.pdf && echo CV-OK
test -f docs/fonts/Clancy-Regular.otf && echo FONTS-OK
test -f docs/images/headshot.jpg && echo HEADSHOT-OK
ls docs/images/software/ | sort
```

Expected: all five `*-OK` lines; software images list the five kept files.

- [ ] **Step 3: Verify each page's key markup**

```bash
grep -c 'hero-name' docs/index.html          # expect 1
grep -c 'class="pubs"' docs/publications.html # expect 1
grep -c 'class="pkg"' docs/software.html      # expect 5
grep -c 'quarto-post' docs/presentations.html # expect >= 8
grep -c 'Clancy' docs/fonts.css               # expect 3
```

- [ ] **Step 4: Human visual check (do not skip)**

Run `quarto preview` (or `open docs/index.html`) and visually compare all four
pages, plus a ~600px-wide window, against
`../astfalck-design-system/ui_kits/website/index.html`. Check: paper
background, Clancy headings, terracotta active-nav underline, section-head ink
rules, hero layout (stacks on mobile), reference-list indents, package rows,
listing rows, footer hairline.

- [ ] **Step 5: Commit the rendered site**

```bash
git add docs
git commit -m "Render site with Astfalck Design System theme

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```
