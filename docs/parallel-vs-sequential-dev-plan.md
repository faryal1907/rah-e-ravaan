# Rah-e-Ravaan — Parallel vs. Sequential Development Guide

**Based on**: `Rah-e-Ravaan_Dev_Steps_Per_Story.docx` + `Rah-e-Ravaan_Development_Plan.docx`  
**Team size assumed**: 3 members — Backend/AI engineer (B), Web frontend engineer (W), Mobile engineer (M)  
**Last updated**: 2026-09-20

---

## How to Read This Document

- **Sequential block** = the entire team is blocked until this is done; no one starts the next phase until it is merged and green.
- **Parallel lanes** = work that can proceed simultaneously across the three members once the preceding sequential block is complete.
- Stories are identified by their Jira key (e.g. `RER-18`). Sprint numbers match the development plan.

---

## Sprint 0 — Project Inception (Week 1)

### Sequential Block A — Must complete together before any feature work
> These are zero-dependency foundation items. Everyone is on the same page before splitting.

| Order | Story | Who leads | Why it must be sequential |
|-------|-------|-----------|--------------------------|
| 1 | **RER-18** Initialize repos & shared conventions | All | Branch strategy, folder layout, and `CONTRIBUTING.md` — every subsequent commit depends on this being agreed and merged. |
| 2 | **RER-24** Draft ER diagram & DB schema v1 | B leads, all review | The schema is the contract every feature reads and writes. No model can be built before this is agreed and Alembic migration runs clean. |
| 3 | **RER-19** Docker Compose local environment | B leads | The compose stack is the shared runtime. CI and local dev both depend on it. |
| 4 | **RER-20** GitHub branch protection + PR/issue templates + CODEOWNERS | All | Branch protection must be live before real feature branches start. Doing this after the first PR defeats the purpose. |
| 5 | **RER-21** CI skeleton (lint + test on every PR) | B leads | The CI job names must exist before they can be added as required status checks in the branch protection rule from RER-20. |

> After Block A is merged, the team splits into three lanes.

---

### Parallel Block 1 — Sprint 0 tail / Sprint 1 start (can run simultaneously)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-22** Provision API keys (Mapbox, OpenAI, Qdrant Cloud, Safepay/JazzCash sandboxes) | **RER-23** Configure web linters (ESLint + Prettier + lint-staged + husky) | **RER-23** Configure mobile linters (`flutter_lints`, `dart format`, `analysis_options.yaml`) |
| | **RER-23** Configure backend linters (Ruff, mypy, Black, pre-commit) | **RER-33** Tailwind design tokens (maroon/lime palette, spacing, radii) | **RER-25** Confirm UX plan → Jira epic traceability; flag any wireframe screens with no story |
| **Unlocks** | All AI/RAG stories; payment gateway stories | All web UI stories | All Flutter stories |
| **Dependency** | Needs Block A merged | Needs Block A merged | Needs Block A merged |

> None of these three lanes touch each other. All can be reviewed and merged in parallel.

---

## Sprint 1 — Authentication & Access Control (Weeks 2–3)

### Sequential Block B — Auth foundation
> Everything downstream reads the `User` model and relies on JWT middleware. Ship this before any feature route is built.

| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-30** JWT issuance + RBAC middleware (`get_current_user`, `require_role`) | B | Every other endpoint in the system uses this dependency. Can't write protected routes without it. |
| 2 | **RER-31** Domain registry data model + `match_domain()` service | B | RER-27 and RER-63 both call this service. Must exist before either is started. |

---

### Parallel Block 2 — Sprint 1 (after Block B)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-29** Admin login + mandatory TOTP 2FA | **RER-26** Customer sign-up form (web) wired to `/auth/signup` and Google OAuth | **RER-26** Customer sign-up screen (Flutter) wired to the same `/auth/*` endpoints |
| | **RER-28** Organizer registration backend (`POST /organizer/apply`, file upload) | **RER-27** Institutional email banner (web, reads `is_institutional` from signup response) | **RER-27** Institutional email banner (mobile) |
| **Depends on** | Block B (JWT/RBAC) | Block B + B finishing `/auth/signup` endpoint | Block B + B finishing `/auth/signup` endpoint |

> W and M are both building UI over the same API. Coordinate on the API contract first (5-min sync); then work independently.

---

## Sprint 2 — Design System & Onboarding (Weeks 4–5)

### Sequential Block C — Component library before screens
> Every screen in every portal uses these primitives. Build them once.

| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-33** Design tokens (Tailwind config finalized, JSON exported for Flutter) | W leads, M consumes | Flutter `ThemeData` is derived from the same token file. Both need this locked before styling any screen. |
| 2 | **RER-34** Shared component library (Button, Card, Input, Badge, ChatBubble, NavShell) | W | Organizer, admin, and customer portals all import these. Build and document before portals diverge. |
| 3 | **RER-35** Destinations table + CRUD API + seed script | B | All discovery, planner, and organizer builder stories read from this table. Seed data must exist for frontend dev and demos. |

---

### Parallel Block 3 — Sprint 2 (after Block C)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | Stretch: begin **RER-41** search index work (`pg_trgm` GIN indexes on `destinations`) | **RER-36** Personalized home/discovery feed skeleton (web): AI hero, trending carousel, group trips section | **RER-70** Mobile auth + onboarding parity: sign-up screen + `flutter_secure_storage` token handling |
| | | **RER-32** Onboarding quiz (4-step wizard, web) wired to `PATCH /users/me/preferences` | **RER-32** Onboarding quiz (Flutter `PageView` wizard, mobile) |
| **Depends on** | Block C | Block C (components) + Block B (auth) | Block C (tokens) + Block B (auth) |

---

## Sprint 3 — Destination Discovery (Weeks 6–7)

### Sequential Block D — Search API before any UI
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-41** Destinations search API with combined filters + trigram indexes | B | Both the web filter panel and the mobile feed call this endpoint. Needs to exist and be tested before UI is wired. |

---

### Parallel Block 4 — Sprint 3 (after Block D)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-40** backend: `GET /destinations/{id}` full detail + weather stub | **RER-37** Search bar with autocomplete (web) | **RER-71** Mobile discovery feed + destination detail screen |
| | Begin **RER-42** embedding ingestion script (Sentence Transformers → Qdrant) | **RER-38** Filter panel (web) | (stretch) Begin adapting discovery for mobile bandwidth: `cached_network_image` |
| | | **RER-39** Mapbox map view with clustered pins (web) | |
| | | **RER-40** Destination detail page (web) | |
| **Depends on** | Block D | Block D | Block D + B finishing `GET /destinations/{id}` |

---

## Sprint 4 — RAG Knowledge Base & Vector Pipeline (Weeks 8–9)

### Sequential Block E — RAG pipeline (backend-only sprint, then hand off)
> This is largely a backend sprint. W and M use the time for catch-up, polish, and stretch items.

| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-42** Embedding ingestion script (Qdrant collection creation, upsert, idempotency) | B | Must exist before the retriever can be built. |
| 2 | **RER-43** RAG retriever service with reranking (LangChain custom retriever) | B | The planner agent (RER-48) wraps this. Must be stable before agent orchestration starts. |
| 3 | **RER-44** Versioned prompt templates + `PromptRegistry` | B | The planner agent loads prompts from this registry. Must exist before RER-48. |
| 4 | **RER-45** Cost-estimator data pipeline + `get_estimated_cost()` service | B | Called by both RER-49 (inline budget) and RER-58 (organizer builder). |

---

### Parallel Block 5 — Sprint 4 (W and M run independently while B builds RAG)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | See Block E above | Polish/bug-fix discovery sprint 3 deliverables; build **RER-34** any missing component library items | **RER-69** Flutter app shell + bottom nav (`go_router`, `BottomNavShell`, placeholder tabs) |
| | **RER-46** Retrieval evaluation harness | Prepare the split-panel layout scaffold for RER-47 (empty panels, state store) | (stretch) Begin **RER-71** catch-up if not done in sprint 3 |
| **Depends on** | Block D | Sprint 3 complete | Block C |

---

## Sprint 5 — AI Conversational Planner, Web (Weeks 10–11)

### Sequential Block F — Planner backend before planner UI
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-48** LangChain agent orchestration + `POST /planner/chat` SSE endpoint + `ItineraryDraft` persistence | B | W and M both build UI on top of this stream. The endpoint contract (SSE events, JSON schema) must be agreed before UI is wired. |

> Agree the streaming event schema in writing (a short ADR or API contract doc) before W/M start wiring.

---

### Parallel Block 6 — Sprint 5 (after Block F endpoint contract is agreed)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-51** English + Urdu input detection (backend planner agent) | **RER-47** Split-panel planner UI (ChatPanel + ItineraryPreviewPanel, Zustand state) | **RER-72** Full-screen mobile AI chat planner (toggle between chat and preview) |
| | **RER-52** backend: shareable link (`POST /itineraries/{id}/share`, `GET /itineraries/shared/{slug}`) | **RER-49** Inline budget estimator (web) | (stretch) begin offline data layer scaffold for sprint 11 |
| | | **RER-50** Partial itinerary re-generation wiring (web diff highlight) | |
| | | **RER-52** Share button + clipboard toast (web) | |
| **Depends on** | Block E | Block F endpoint + Block E | Block F endpoint + Block E |

---

## Sprint 6 — Itinerary Management & Collaboration (Weeks 12–13)

### Sequential Block G — Trips API before trip UI
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-53** `GET /trips?status=` endpoint | B | My Trips tab (web + mobile) both call this. |
| 2 | **RER-54** `GET /trips/{id}` full detail + packing list service | B | Trip detail page (web + mobile) depends on this. |

---

### Parallel Block 7 — Sprint 6 (after Block G)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-55** backend: `TripCollaborator` model, invite + accept endpoints, suggestions workflow | **RER-53** My Trips tab UI (web): tabs + trip cards | **RER-53** My Trips tab (Flutter): tabs + trip cards |
| | **RER-56** backend: PDF export (Jinja2 template + WeasyPrint, `GET /trips/{id}/export.pdf`) | **RER-54** Trip detail page (web): timeline, Mapbox route, packing checklist | **RER-54** Trip detail screen (Flutter): timeline + map |
| | | **RER-55** Invite modal + suggestions panel (web) | |
| | | **RER-56** Download PDF button (web) | |
| **Depends on** | Block G | Block G | Block G |

---

## Sprint 7 — Organizer Portal Core + FYP-I Demo Prep (Weeks 14–15)

### Sequential Block H — Organizer backend before organizer UI
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-57** `GET /organizer/dashboard` + `GET /organizer/activity` | B | Organizer dashboard UI depends on this. |
| 2 | **RER-58** `POST/PUT /organizer/itineraries` (nested day/stop, visibility, price) | B | Itinerary builder UI depends on this. |
| 3 | **RER-59** `GET /organizer/trips/{id}/participants` + approve/reject + CSV export | B | Participants table UI depends on this. |

---

### Parallel Block 8 — Sprint 7 (after Block H)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-60** Seed demo data script (`seed_demo_data.py`) | **RER-57** Organizer dashboard UI: stat cards + activity feed | **RER-70** Mobile auth + onboarding parity (if not completed in sprint 2) |
| | FYP-I demo rehearsal support | **RER-58** Itinerary builder UI: drag-and-drop stops, live map, AI-assist button | Polish mobile discovery + planner from sprint 4–5 |
| | | **RER-59** Participants table UI: bulk actions, CSV download | FYP-I demo rehearsal on mobile device |
| | | FYP-I demo script + slides | |

> **▶ FYP-I MILESTONE** — Demo of customer AI planner, discovery, trip management, organizer portal. All hands on rehearsal by end of week 15.

---

## Sprints 8–9 — Admin + Domain Locking (Weeks 16–19)

### Sequential Block I — Domain enforcement before admin UI
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-63** Enrollment-time domain re-check enforcement (server-side 403 logic in `POST /trips/{id}/enroll`) | B | Must exist and be tested before admin UI approves domains, to prove enforcement is real, not cosmetic. |
| 2 | **RER-61** `GET/POST /admin/organizers` approval queue endpoints | B | Admin approval queue UI depends on these. |
| 3 | **RER-62** `GET/POST/PATCH /admin/domains` registry endpoints | B | Domain registry UI depends on these. |
| 4 | **RER-64** Transactional email service (`send_email()` wrapper + templates) | B | Approval/rejection emails fire from the endpoints built above. |

---

### Parallel Block 9 — Sprints 8–9

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-65** Admin dashboard backend metrics endpoint | **RER-61** Admin organizer approval queue UI | **RER-11** (Sprint 10 prep) Begin Flutter app shell polish; write widget tests for auth + onboarding screens already built |
| | **RER-66** Flag model + moderation service + 3-strikes auto-suspend | **RER-62** Domain registry UI | |
| | **RER-67** Advisory model + `POST /admin/advisories` | **RER-63** Enrollment block UX (web: show 403 error clearly) | |
| | **RER-68** Feature flags, prompt template editor endpoints, audit-log | **RER-64** Rejection/approval email trigger wiring (web form → endpoint) | |
| | | **RER-65** Admin dashboard UI | |
| | | **RER-66** Moderation queue UI | |
| | | **RER-67** Advisory banner component + publishing form | |
| | | **RER-68** System config tabbed console (web) | |

---

## Sprint 10 — Mobile App Foundation (Weeks 20–21)

### Sequential Block J — Mobile baseline (M-heavy sprint, B/W support)
> This sprint is primarily M's sprint. B and W are unblocked to continue their own work.

| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-69** Flutter app shell + bottom nav (if not done in sprint 4 stretch) | M | Every other mobile screen hangs off this router. |
| 2 | **RER-70** Mobile auth + onboarding (if not done in sprint 2 stretch) | M | Auth tokens must be stored securely before any other screen makes authenticated API calls. |

---

### Parallel Block 10 — Sprint 10

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | Begin **RER-73** SQLite schema design (collaborate with M on repository layer interface) | Begin Sprint 14 prep: research `react-i18next` setup for Urdu localization | **RER-71** Mobile discovery feed + destination detail (if sprint 3 stretch wasn't finished) |
| | | Polish admin console from sprint 9 | **RER-72** Full-screen mobile AI chat planner (if sprint 5 stretch wasn't finished) |
| | | | Generate typed API client from OpenAPI spec for Flutter |

---

## Sprint 11 — Offline-First Architecture (Weeks 22–23)

### Sequential Block K — Local DB before sync service
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-73** SQLite local store (`sqflite`/`drift`, repository layer, map tile caching) | M | The sync service (RER-75) writes to this store. Download flow (RER-74) also needs it. Must exist first. |

---

### Parallel Block 11 — Sprint 11 (after Block K)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | Prepare GPS endpoints scaffold (RER-79 backend) for sprint 12 | (Sprint 12 prep) Build Mapbox breadcrumb map component (read-only, for parent view) | **RER-74** Download itinerary + maps flow + offline indicator |
| | | | **RER-75** Background sync service (reconnect listener, batch upload, last-write-wins conflict) |
| | | | **RER-76** Last-synced timestamp labels |

---

## Sprint 12 — Store-and-Forward GPS Tracking (Weeks 24–25)

### Sequential Block L — GPS logging before sync, sync before dashboard
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-77** Background GPS logging service (Flutter foreground service, `gps_logs` SQLite table) | M | RER-78 (battery scaling) modifies the interval this service uses. RER-79 (mobile sync) reads from this table. Must exist first. |
| 2 | **RER-79** backend: `POST /gps/sync` upsert endpoint + `GET /gps/trips/{id}/breadcrumbs` | B | The mobile sync service and the parent/organizer breadcrumb views all call these endpoints. Must be agreed and deployed to staging before UI is built. |

---

### Parallel Block 12 — Sprint 12 (after Block L)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-81** backend: `TrackingConsent` model + invite/revoke/access-check logic | **RER-82** Organizer group GPS dashboard (Mapbox live map, participant cards, signal-loss alert) | **RER-78** Battery-aware interval scaling |
| | **RER-82** `GET /organizer/trips/{id}/gps-overview` endpoint | **RER-81** Parent breadcrumb map (read-only web view) | **RER-79** Mobile GPS sync service (upload `synced=false` rows on reconnect) |
| | **RER-83** Missed check-in push notification job (FCM integration) | | **RER-80** Customer live tracking screen |
| | **RER-84** GPS data retention job (30-day delete after trip end) | | **RER-81** Consent invite flow (mobile) |

---

## Sprint 13 — Bookings & Payments (Weeks 26–27)

### Sequential Block M — Payment models before any gateway work
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-85** `Accommodation` + `TransportOption` models + `GET /bookings/search` endpoint | B | Booking search UI depends on this data existing. |
| 2 | **RER-86** Payment gateway integration (Safepay + JazzCash, `Payment` model, webhook handler) | B | Booking confirmation (RER-87) and organizer revenue (RER-88) both depend on the `Payment` table being populated. |

---

### Parallel Block 13 — Sprint 13 (after Block M)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-87** backend: confirmation email + SMS + refund flow | **RER-85** Booking search/results UI (web + trip detail integration) | **RER-85** Booking search screen (Flutter) |
| | **RER-88** `GET /organizer/revenue` + `Payout` model | **RER-86** Checkout flow UI (Safepay redirect, JazzCash flow) | **RER-86** Mobile checkout flow |
| | **RER-89** Admin payments console endpoints | **RER-87** Booking status + refund tracking UI | |
| | | **RER-88** Organizer revenue dashboard + payout history | |
| | | **RER-89** Admin financials console UI | |

---

## Sprint 14 — Notifications, Accessibility & Localization (Weeks 28–29)

> This is a cross-cutting sprint. All three lanes work on different concerns simultaneously with no hard sequential dependency between them after the notification WebSocket endpoint exists.

### Sequential Block N
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-90** WebSocket `/ws/notifications` endpoint + Redis pub/sub backend | B | Web and mobile notification UIs both subscribe to this. Must be live in staging before UI is built. |

---

### Parallel Block 14 — Sprint 14

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-90** Notification trigger services (weather alert checker, advisory hook, booking reminder scheduler, companion-activity publisher) | **RER-90** Notification bell + inbox UI (web) | **RER-90** Push notification integration (FCM for mobile, notification inbox screen) |
| | **RER-93** Redis caching pass on hot endpoints + query profiling | **RER-91** `react-i18next` setup + Urdu locale file + RTL rendering pass | **RER-91** `flutter_localizations` + Urdu ARB file + Noto Nastaliq Urdu font + RTL pass |
| | | **RER-92** axe-core accessibility scan + fixes; screen-reader manual pass | **RER-92** Tap target size audit (44×44px minimum) on all mobile screens |

---

## Sprint 15 — Hardening, Security & QA Regression (Weeks 30–31)

### Sequential Block O — Security before E2E (don't write E2E over broken auth)
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-95** Dependency vulnerability scan (`pip-audit`, `npm audit`, flutter CVE check) + secrets scanning (`gitleaks` in CI) + RBAC penetration pass | All | Fix security holes before writing E2E tests that run against real endpoints. Saves rewriting tests after a security fix changes behavior. |

---

### Parallel Block 15 — Sprint 15 (after Block O)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-96** Load testing (k6/Locust): planner endpoint, GPS sync bursts, search under concurrency | **RER-94** Playwright E2E suite: AI trip planning, institutional enrollment, organizer publishing, admin approval | **RER-94** Flutter `integration_test` E2E: mobile equivalents of the five key flows |
| | **RER-95** Rate limiting (Redis-backed per-IP/per-user on auth + planner endpoints) | **RER-97** Bug bash: web portal — log all findings in Jira with P0–P3 severity | **RER-97** Bug bash: mobile app |
| | **RER-97** Bug bash triage + fix P0/P1 issues | Fix P0/P1 web bugs | Fix P0/P1 mobile bugs |

---

## Sprint 16 — Production Deployment & FYP-II (Weeks 32–33)

### Sequential Block P — Deploy before monitoring, monitor before demo
| Order | Story | Who leads | Why sequential |
|-------|-------|-----------|----------------|
| 1 | **RER-98** Production deployment (Railway/Render backend, Vercel web, managed DB/Redis/Qdrant, `alembic upgrade head` against prod DB) | B leads, all verify | Everything else in this sprint assumes a live production URL exists. |
| 2 | **RER-99** Monitoring + alerting (Sentry across all three apps, uptime checks, log aggregation) | B | Can't rehearse the demo against a system that isn't observable. Set up monitoring before rehearsal so failures are caught. |

---

### Parallel Block 16 — Sprint 16 (after Block P)

| | Member B — Backend/AI | Member W — Web | Member M — Mobile |
|---|---|---|---|
| **Stories** | **RER-100** Architecture document + API reference + FYP report appendix | **RER-100** User manual (customer, organizer, admin sections) with screenshots | Submit final signed Android/iOS builds to internal test track |
| | FYP-II demo rehearsal (backend scenarios + fallback plan) | FYP-II demo rehearsal (web portal flows) | **RER-101** FYP-II demo rehearsal (mobile flows) |
| | | | **RER-100** Mobile-specific notes in user manual |

> **▶ FYP-II MILESTONE** — Final evaluation, live production demo, project defense.

---

## Summary: Sequential Blocks at a Glance

| Block | Stories | Reason it can't be parallelized |
|-------|---------|--------------------------------|
| **A** | RER-18, RER-24, RER-19, RER-20, RER-21 | Repo + schema + CI are shared infrastructure; nothing else is buildable without them |
| **B** | RER-30, RER-31 | JWT/RBAC and domain model are used by every other backend service |
| **C** | RER-33, RER-34, RER-35 | Design tokens, component library, and seed destinations are consumed by all UI stories |
| **D** | RER-41 | Search API is called by both web filter panel and mobile feed |
| **E** | RER-42 → RER-43 → RER-44 → RER-45 | RAG pipeline is a strict chain: embeddings → retriever → prompts → cost estimator |
| **F** | RER-48 | Planner backend endpoint contract must be agreed before web and mobile wire to it |
| **G** | RER-53, RER-54 | Trips API is called by web and mobile trip views simultaneously |
| **H** | RER-57, RER-58, RER-59 | Organizer endpoints underpin all organizer UI work |
| **I** | RER-63, RER-61, RER-62, RER-64 | Domain enforcement must be proven before admin UI activates it; emails fire from the same endpoints |
| **J** | RER-69, RER-70 | Mobile router and auth must exist before any other screen is navigable |
| **K** | RER-73 | SQLite store must exist before sync service and download flow write to it |
| **L** | RER-77, RER-79 (backend) | GPS logger feeds the sync table; sync backend must exist before any GPS UI is wired |
| **M** | RER-85, RER-86 | Booking and payment models must exist before confirmation, revenue, and admin flows |
| **N** | RER-90 (WebSocket endpoint) | Notification subscribers (web + mobile) need a working endpoint to connect to |
| **O** | RER-95 (security pass) | Fix auth/RBAC holes before E2E tests encode the (possibly broken) behavior |
| **P** | RER-98, RER-99 | Production must be live and observable before the demo can be rehearsed against it |

---

*Rah-e-Ravaan · BSCS FYP · Confidential Draft*
