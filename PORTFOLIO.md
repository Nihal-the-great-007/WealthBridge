# WealthBridge — Portfolio Showcase

## Project at a Glance

| | |
|---|---|
| **Project Name** | WealthBridge |
| **Tagline** | Bridging Today's Income with Tomorrow's Retirement |
| **Type** | Full-Stack Financial Web Application + PWA |
| **Domain** | FinTech · Actuarial Science · Retirement Planning |
| **Stack** | Python · FastAPI · Vanilla JS · Chart.js · PWA |
| **Deployment** | Vercel (Serverless Python) |
| **Status** | ✅ Production Ready |

---

## What We Built

WealthBridge is a **premium interactive retirement corpus planning dashboard** for Indian professionals. It unifies four separate retirement savings vehicles — EPF, NPS, ELSS, and WeCare DB Pension — into a single actuarial engine, running **2,000-iteration Monte Carlo simulations** to show the probability of retirement success under varying market conditions.

### The Gap We Identified

Indian professionals have retirement money sitting in **four siloed, incompatible instruments**, with no unified tool to see their complete financial picture. Existing tools either focus on one instrument, use oversimplified linear projections, or ignore longevity risk entirely.

### Our Solution

We built an end-to-end platform that:
- **Integrates** all four retirement vehicles with actuarially-correct formulae
- **Simulates** 2,000 random market scenarios (Monte Carlo) to produce P10/P50/P90 outcomes
- **Visualises** the complete 32-year journey interactively
- **Runs anywhere** — browser, mobile, installable as a PWA

---

## Technical Highlights

### Financial Engine (Python / NumPy)
- Parses four structured CSV data files exported from the WeCare Excel model
- Computes EPF accumulation with compound interest and employer matching
- Models NPS blended returns across equity/debt/alt allocation
- ELSS corpus with 13% gross → 12% net, 4% SWR sustainable drawdown
- WeCare DB pension using defined-benefit formula with 33% commutation
- **Monte Carlo**: 2,000 iterations, normally-distributed market shocks, success probability

### Backend (FastAPI)
- `GET /api/data` — base-case projections from loaded CSV assumptions
- `POST /api/calculate` — recalculate with user-defined parameter overrides
- Fully typed with Pydantic request/response models
- Vercel serverless-compatible (zero-infrastructure deployment)

### Frontend (Vanilla JS SPA)
- Zero framework dependencies — pure HTML/CSS/JavaScript
- Three-tab single-page application with animated panel transitions
- Real-time chart updates via Chart.js 4.4.3 (Monte Carlo fan, salary bar, corpus donut, corpus line)
- Full print/PDF export with `@media print` + `beforeprint`/`afterprint` JS hooks
- CSV export with structured financial report

### Design System
- **Glassmorphism** UI: `backdrop-filter: blur()` + translucent panels on beige background
- **Dual theme**: Bright Mode (default) with animated beige guilloche canvas, Dark Mode
- **144Hz smooth**: GPU-promoted layers (`will-change`, `transform3d`), spring `cubic-bezier`, RAF-debounced updates
- **Startup screen**: Full-screen animated guilloche wave canvas (pure JavaScript/Canvas API)

### Progressive Web App
- Full PWA with `manifest.json`, `sw.js` service worker
- Offline caching (stale-while-revalidate strategy)
- Installable on Android (Add to Home Screen prompt) and iOS (Safari Share flow)
- Multi-size icons: 16/32/48px favicon.ico, 192px, 512px PNG, 180px Apple touch icon
- Open Graph + Twitter Card meta for social/search preview

---

## Key Metrics

```
Base Case: Age 28 → 60 | ₹20,00,000 Starting CTC | 8% salary growth
───────────────────────────────────────────────────────────────────────
Total Retirement Corpus:   ₹36.20 Crore
Monthly Retirement Income: ₹1,43,688 / month
Income Replacement Ratio:  ~62%
Monte Carlo Success Rate:  89.6% (survives to age 85, 2,000 simulations)
Simulation Engine:         2,000 stochastic market paths per calculation
Data Horizon:              32-year salary + corpus projection (year-by-year)
```

---

## Contributors & Attribution

> *"The WeCare Plan and the Excel-based financial model, including future salary trajectory projections and retirement corpus calculations, were jointly developed by **Nihal Patil** and **Anant Bokade**. Based on this financial model, the Unified Financial Calculator was collaboratively developed in Python, with development assistance from **Anti-Gravity AI**. Both contributors had an equal role in the design, development, testing, and validation of the project."*

| Role | Contributor |
|---|---|
| Co-Author · Financial Model Design | **Nihal Patil** |
| Co-Author · Financial Model Design | **Anant Bokade** |
| AI Development Assistance | Anti-Gravity AI (Google DeepMind) |

---

## Skills Demonstrated

- **Actuarial Financial Modelling** — EPF/NPS/ELSS/DB pension formulae
- **Stochastic Simulation** — Monte Carlo with NumPy random sampling
- **Full-Stack Python Web Dev** — FastAPI, Pydantic, Uvicorn, Pandas
- **Modern Frontend Engineering** — CSS custom properties, glassmorphism, Canvas API
- **Data Visualisation** — Chart.js, multi-chart dashboards, print-quality PDF export
- **Progressive Web Apps** — Service Worker, offline-first, PWA installability
- **Performance Engineering** — GPU compositing, 144Hz animation, RAF debouncing
- **DevOps / Deployment** — Vercel serverless Python, `vercel.json` configuration
- **UX / Product Design** — Dual theme, mobile-first responsive, startup animations

---

*Built with Python, FastAPI, Vanilla JS, Chart.js · Deployed on Vercel*
*© 2026 Nihal Patil & Anant Bokade — MIT Licence*
