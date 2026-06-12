# CLAUDE.md

## Overview

This repository is the marketing website for **O Williams Consulting**, an IT &
cybersecurity consulting firm serving the DC / Maryland / Virginia (DMV) area. It is a
single-page, fully static site built as one self-contained HTML file with inline CSS and
vanilla JavaScript — no build step, no framework, and no dependencies. It is published via
**GitHub Pages** from the `main` branch and served on the custom domain in `CNAME`
(`owilliamsconsulting.com`).

## Repository layout

| Path           | Purpose                                                                 |
| -------------- | ----------------------------------------------------------------------- |
| `index.html`   | The entire site: markup, design tokens + CSS (in `<style>`), and JS (in `<script>`). Everything lives here. |
| `favicon.svg`  | Site icon (inline SVG), referenced from `index.html`.                   |
| `CNAME`        | GitHub Pages custom domain (`owilliamsconsulting.com`). Do not remove.  |
| `README.md`    | One-line project description.                                            |

There is no `src/`, no `package.json`, no lockfile, and no `.github/` workflows.

## Build / test / run / lint

There is **no build, test, or lint tooling** in this repo — it is plain static HTML.
Do not invent npm scripts or a bundler; there is nothing to compile.

- **Preview locally** — open `index.html` directly in a browser, or serve the folder:
  ```bash
  python3 -m http.server 8000   # then visit http://localhost:8000
  ```
- **Build:** none required. The deployed artifact is the source file itself.
- **Test / lint:** none configured.
- **Deploy:** push to `main`; GitHub Pages serves the repo root automatically.

## Architecture notes

The page is a top-to-bottom static layout. Sections in `index.html`, in order: nav/header,
hero, services, about/values, why-us, CTA/contact, footer. In-page navigation uses anchor
links (`#services`, `#about`, `#why-us`, `#contact`).

Three small vanilla-JS features live in the bottom `<script>` block:
- **Theme toggle** — switches `data-theme` (`light`/`dark`) on `<html>`; initial value
  follows `prefers-color-scheme`.
- **Mobile menu** — hamburger toggles the `.open` class on the mobile nav.
- **Scroll reveal** — an `IntersectionObserver` adds `.visible` to elements with `.reveal`.

## Conventions & gotchas

- **Everything is in `index.html`.** CSS and JS are inline; edit them there rather than
  adding external files unless you intend to change the project's single-file structure.
- **Theming uses CSS custom properties** defined under `:root` / `[data-theme="light"]`,
  with overrides under `[data-theme="dark"]` and a `prefers-color-scheme` fallback. Prefer
  existing design tokens (`--color-*`, `--space-*`, `--text-*`, `--radius-*`) over hardcoded
  values, and keep light/dark in sync when adding colors.
- **Fonts** (Satoshi, Cabinet Grotesk) load from the Fontshare CDN via `<link>`; they
  require network access and have local fallbacks in `--font-body` / `--font-display`.
- **Google Tag Manager** (`GTM-5FJJTJKZ`) is wired in the `<head>` and `<body>` (noscript).
  Preserve both snippets if you keep analytics.
- **Accessibility** is intentional: skip link, ARIA labels/roles, `aria-hidden` on
  decorative SVGs, and a `prefers-reduced-motion` block. Maintain these when editing markup.
- **`CNAME` controls the live domain** — changing or deleting it affects production hosting.
