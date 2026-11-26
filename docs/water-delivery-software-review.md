# Water delivery software: case-study evidence

Initial source: a read-only browser-review brief supplied by the owner. On November 25, 2026, the owner authorized headless Chromium capture; authenticated read-only inspection of the demo application then confirmed the order-management and canal flow-history views. Application: `https://order.kerrco.us`.

## Owner clarification — November 25, 2026

The owner confirmed that `order.kerrco.us` contains test data, with no operational data, and authorized adding more test data. This resolves the earlier uncertainty about whether the displayed records were real. The additive demonstration batch was populated earlier that day. Authenticated screenshots of its current orders and canal flow history are now included in the website.

## Observed interface features

- User order lists grouped as running, pending, rejected, and completed.
- A scheduling form with headgate selection, turn-on/off dates and amounts, order date, and owner. Turn-on amount is labeled “Acre-Feet per 12h.”
- Individual order details with edit and delete controls visible but unused.
- Administrator pending-request views with Approve and Reject controls.
- Administrator current/past order lists and a rejection-reason column on the dashboard.
- Canal and headgate capacity, operating status, latest recorded flows, and flow-history charts and tables.
- Announcement management with publication status and creation, editing, and deletion controls.

## Interpretation and limits

The interface suggests a workflow of preparing a headgate delivery request, administrative review, and viewing current/historical orders. Coordinating requests by headgate, requested dates, and amounts is a reasonable description of its purpose. The previous process and its shortcomings are not established.

No submission, approval transition, physical delivery, edit, deletion, or announcement change was tested. Visible controls establish interface features rather than verified end-to-end behavior. Do not claim automated gate operation, telemetry integration, capacity enforcement, savings, performance, or other outcomes.

## Owner confirmations still needed

- Exact roles, headgate access rules, scheduling cutoffs, capacity checks, and rejection handling.
- Whether recorded flow readings are manual or integrated with equipment, and whether scheduling controls physical gates.
- Correct customer identity and permission to publish it; header and footer reportedly show different company names.
- One displayed test request reportedly has a turn-off date before its turn-on date; validation behavior was not tested. This remains a follow-up question, not a diagnosed defect.
- Precise implementation responsibilities, technology stack, and evidence for any measurable results. The owner previously confirmed building the software; no narrower role or stack is inferred.

## Screenshot evidence — November 25, 2026

The owner explicitly authorized installed headless Chromium after the normal browser connection remained unavailable. The capture used the application's publicly displayed demo login and visited only the order-management and canal detail pages. No order, approval, rejection, announcement, or account setting was changed.

- `web/assets/img/rework/irrigation-orders-screen.jpg` — 1440 × 700; actual current-order table showing fictional demo users, headgates, dates, and requested amounts.
- `web/assets/img/rework/irrigation-canal-screen.jpg` — 1440 × 1100; actual Demo Orchard Canal capacity/status, rendered flow-history chart, and recorded readings.

The captures show actual rendered application UI and are not mockups. Browser framing selects the relevant content; no data, labels, or controls were altered. Captions identify the records as test data and the capture date. Credentials are absent from the screenshots and were not saved with the capture artifacts.

The homepage includes an Irrigation Scheduling tab and a persistent case-study thumbnail. The portfolio includes the current-orders capture, and the case study includes both images with full-size links and text descriptions. Weather remains the initial homepage project.

Capture metadata and source images are retained under ignored `artifacts/irrigation-captures-2026-11-25/published/`. Marketing-page browser checks at 1440, 768, 375, and 320px passed for the three affected pages, including loaded images, no horizontal overflow, project-tab keyboard navigation, no-JavaScript content, and thumbnail/full-size navigation. This does not establish full accessibility certification or physical delivery behavior.
