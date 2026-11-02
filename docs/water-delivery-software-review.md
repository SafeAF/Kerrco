# Water delivery software: case-study evidence

Source: read-only browser-review brief supplied by the owner in this conversation. This implementation did not independently inspect the authenticated application. Application: `https://order.kerrco.us`.

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
- Whether displayed records are demo data. One displayed request reportedly has a turn-off date before its turn-on date; validation behavior was not tested. This is a follow-up question, not a diagnosed defect.
- Precise implementation responsibilities, technology stack, and evidence for any measurable results. The owner previously confirmed building the software; no narrower role or stack is inferred.

## Screenshot plan

No publishable screenshots were supplied or added to the website. Reviewed screens contain identifiers, contact information, or operational figures with unconfirmed demo status.

Potential captures, after verifying fictional data and publication permission:

1. User order overview showing multiple statuses.
2. Delivery-request form with fictional headgate and owner.
3. Administrator approval queue.
4. Canal/headgate flow-history screen.

The current public-facing draft uses only the observed features above, a read-only review qualification, and the owner-confirmed project attribution. Customer identity, screenshots, credentials, and unsupported outcome claims are omitted.
