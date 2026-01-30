# Job Application Tracker — Specification

## 1. Purpose

A local, single-user system to track job applications as a **pipeline** rather than a list.

The system must:
- Log every application
- Preserve a full event history
- Provide actionable visibility via Kanban, timelines, and analytics

The system is not:
- A resume builder
- A job board
- A productivity app

---

## 2. Non-Goals

- Multi-user support
- Authentication / authorization
- Cloud deployment
- Email ingestion (initially)
- Mobile support

---

## 3. Tech Stack

- Backend: FastAPI (async)
- ORM: Tortoise ORM
- Database: SQLite (file-based)
- Templating: Jinja2
- Frontend: Server-rendered HTML + minimal vanilla JS
- Charts: Server-side computed, rendered as HTML/SVG

---

## 4. Domain Model

### 4.1 Application

Represents a single job application.

**Fields**
- id (int, PK)
- company (string, required)
- role_title (string, required)
- location (string, optional)
- source (string, optional)
- date_applied (date, required)
- status (enum, required)
- salary_min (int, optional)
- salary_max (int, optional)
- relocation (bool, optional)
- visa_sponsorship (enum: yes/no/unknown)
- notes (text, optional)
- last_updated (datetime, auto)

**Status enum**
- draft
- applied
- interview
- offer
- rejected
- withdrawn

---

### 4.2 ApplicationEvent

Immutable log of meaningful events.

**Fields**
- id (int, PK)
- application_id (FK → Application)
- event_type (enum)
- event_date (datetime)
- metadata (JSON, optional)

**Event types**
- applied
- recruiter_message
- interview_scheduled
- interview_completed
- follow_up_sent
- rejection
- offer_received
- offer_accepted
- withdrawn

Events must never be edited or deleted.

---

## 5. Core Invariants

- Every application must have at least one `applied` event
- `Application.status` reflects the *latest meaningful event*
- Analytics must be derivable from events alone
- Deleting an application deletes all its events

---

## 6. Pages

### 6.1 Kanban Board (`/`)

Primary daily view.

**Columns**
- Draft
- Applied
- Interview
- Offer
- Rejected
- Withdrawn

**Each card shows**
- Company
- Role title
- Location
- Days since last update

**Actions**
- Create application
- Change status (optional drag/drop or button)

---

### 6.2 Application Timeline (`/applications/{id}`)

Detailed inspection view.

**Displays**
- Application summary
- Vertical timeline of all events (chronological)
- Notes
- Add new event form

---

### 6.3 Analytics (`/analytics`)

System health view.

**Metrics**
- Applications per week
- Interview callback rate
- Offer rate
- Median response time
- Ghost rate (no response > N days)

All metrics computed server-side.

---

## 7. API Endpoints (Internal)

Used by templates and optional JS.

### Applications
- `POST /applications`
- `GET /applications`
- `GET /applications/{id}`
- `PATCH /applications/{id}`

### Events
- `POST /applications/{id}/events`
- `GET /applications/{id}/events`

No public API guarantees.

---

## 8. Analytics Definitions

### Response Time
Time between:
- `applied` event
- first of: recruiter_message, interview_scheduled, rejection

### Ghosted Application
- Has `applied` event
- No other events
- `now - date_applied > 14 days`

### Callback Rate
applications with interview_scheduled
/
total applied applications



---

## 9. Data Lifecycle

- Local SQLite DB
- No migrations initially
- Schema changes may invalidate old DB
- Data export via CSV (optional)

---

## 10. UX Principles

- Fast to log
- No modal chains
- No hidden state
- No gamification

The system exists to **reduce cognitive load**, not add it.

---

## 11. Success Criteria

The system is successful if:
- Logging an application takes < 30 seconds
- You can answer “what should I follow up on?” in < 10 seconds
- Rejections feel like data, not judgment

---

## 12. Future Extensions (Out of Scope)

- Email ingestion
- Browser extension
- CV version tracking
- Reminder system
- PostgreSQL migration

These must not influence current design.

