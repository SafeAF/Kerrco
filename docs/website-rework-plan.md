# KERRCO website rework plan

Date: November 2, 2026
Status: Software-led site and evidence-based case-study draft implemented locally; owner confirmations and visual release review remain open.
Scope: Rework the static site in `web/`, review locally, and prepare for the existing hosting environment. Publication is a separate step.

## 1. Direction

Lead with **software, workflow automation, and practical AI consulting for small businesses**, with a free initial consultation. The owner no longer operates the construction company.

The farm, workshop, woodwork, and past construction portfolio show the broad hands-on background behind the software work. They support the main offer rather than appearing as equal service lines. Do not advertise construction services, farm services, or woodwork sales.

Keep the KERRCO name and Twin Falls identity. Write in an owner-led voice and avoid implying a large team. The shared story is understanding how work happens, paying attention to details, and building useful tools.

This direction supersedes the original three-service concept. `docs/REVAMP-PLAN-CODEX.md` and `docs/strategy/local-ai-consulting.md` remain background references.

## 2. Visitor path and site structure

The main route is **software offer → real project proof → consultation request**. The background portfolio helps visitors understand the person doing the work.

Navigation: **Software & AI · Software project · My background · Contact**, with the wordmark linking home and a prominent free consultation link.

| Page | Purpose |
| --- | --- |
| `index.html` | Software-first introduction, live software proof, three software offers, consultation, and selected background work |
| `software-ai.html` | Explain custom software, automation, AI use cases, and the approach to a project |
| `water-delivery-software.html` | Case-study draft covering the observed request, review, order-status, flow-history, and announcement interfaces; link to the production application |
| `background.html` | Owner introduction, farm/workshop photography, grouped woodwork gallery, and past construction work |
| `contact.html` | Free consultation request, useful information to include, expectations, and visible email fallback |
| Three existing `*-project-details.html` pages | Preserve URLs and project facts, present work as historical, and use the shared design |
| `404.html` | Recover to home, software, or contact using the shared design |

Separate construction-service and woodwork-sales pages are outside this revised scope. Background sections have direct `#farm`, `#woodwork`, and `#construction` destinations.

## 3. Software content

Homepage headline: **Practical software. Hands-on perspective.**

Explain the offer through possible projects, not unverified completed-client claims:

- Custom business applications, scheduling, and order tracking.
- Reducing duplicate entry and organizing incoming requests and follow-up work.
- Searchable business documents and draft summaries for staff review.

Describe the approach: understand the workflow, choose a practical solution, then agree on a focused scope and try it in the real workflow. Existing tools or straightforward automation may be more useful than AI.

Do not promise specific savings, integrations, certifications, customer outcomes, or nationwide service without confirmation.

### Water delivery scheduling software

Confirmed by the owner: KERRCO built water delivery scheduling software, live at `https://order.kerrco.us`.

The owner supplied a read-only browser-review brief. The project page now describes observed user/admin interfaces and the workflow they suggest. The homepage and software offer page use a shorter version of the same supported feature description. Sign-in is required for the reviewed screens; do not advertise an open demo.

The authenticated review was performed outside this implementation session; its evidence and limits are recorded in `docs/water-delivery-software-review.md`. Request submission, approval transitions, and physical delivery were not tested. Before adding further claims, confirm:

- The previous process and its shortcomings, exact user roles, access rules, scheduling cutoffs, capacity enforcement, and rejection handling.
- Whether flow readings are manual or equipment-integrated, and whether scheduling controls physical gates.
- Customer naming permission, if a name is included.
- Approved screenshots with synthetic or sanitized data.
- Precise implementation responsibilities, technology stack, and evidence for any outcome claims.
- Whether reviewed records are demo data, including the reported inconsistent turn-on/off dates. No validation defect has been diagnosed.

Credentials are not stored in repository files. No screenshots were retained for publication because their identifiers and operational data have unconfirmed demo status. Customer naming remains excluded; the supplied brief reported different company names in the header and footer. Screenshots and additional claims can follow owner confirmation without blocking review of the current text-based case study.

### Future document-search demo

Keep the RAG demo out of launch requirements. When ready, use public or synthetic documents and show a representative question, supporting sources, and an honest no-answer state. Do not show disabled buttons or empty placeholders now.

## 4. Background and photography

Use farming, making things, and past construction to explain the practical perspective behind the software work.

- Keep original photos intact; use optimized web copies without upscaling.
- Selected farm photos show hay bales, cattle, and a tractor-rebuild component.
- The background woodwork gallery contains six pieces: walnut bowl, deep walnut bowl, spalted birch bowl, apricot bowl, apricot serving piece, and walnut chest.
- Group alternate views of the two walnut bowls with native expandable controls. Larger images open directly and work without JavaScript.
- Material names follow supplied filenames; owner review remains required before publication. Do not derive dimensions, food-safety claims, availability, prices, or shipping policies from filenames or photos.
- Preserve the three construction detail URLs, original project facts, and all existing project photographs. Explain that the construction company is no longer operating.
- Caption images, supply descriptive alt text and real dimensions, and lazy-load photography below the opening view.

Reviewed the original 11 woodwork photos during the first implementation, then all 15 farm photos and four additional workshop/woodwork photos during the software-first revision.

## 5. Consultation and contact

The initial conversation is free. Ask about the business, workflow causing trouble, and what a useful improvement would look like. A recommendation or separately scoped project may follow.

Use the existing address, **kerrcoenterprises@gmail.com**, with contextual subjects for a free consultation or software project. Consultation links open an editable email outline. Always display the address for copying.

Clearly explain that email links open the visitor's email app. Do not claim an appointment was booked, a message was delivered, or a form was submitted. Do not promise a call duration, response time, or free implementation.

The live site pages do not load or submit to the legacy PHP handlers. A delivered form is a later hosting decision requiring real delivery and failure-path tests.

## 6. Design and technical approach

- Retain static HTML/CSS and the `web/` deployment root; no framework or CMS.
- Use `web/assets/css/home.css` across all nine pages.
- Keep charcoal/navy, warm off-white, restrained gold, and the KERRCO wordmark.
- Provide accessible navigation, a skip link, visible focus, reduced-motion behavior, and mobile layout rules.
- Keep essential content and galleries usable without JavaScript, animation, hover, or a preloader.
- Old template CSS, JS, and vendor assets remain in the repository but are no longer loaded by these pages. Do not remove original assets as part of this milestone.
- Each page has its own title, description, and sharing metadata. A 1200 × 630 branded JPEG supports software-page sharing. Final absolute sharing URLs and canonical metadata need the confirmed production website origin.

## 7. Implementation checklist

### Milestone 1 — Software-led homepage

- [x] Build the homepage and honest email inquiries.
- [x] Revise positioning to software first, with construction as past experience.
- [x] Review farm photos and prepare selected derivatives.
- [x] Owner accepted the software-first direction and local appearance.
- [ ] Complete agent desktop/mobile visual and keyboard review; browser automation remains unavailable.

### Milestone 2 — Complete visitor paths

- [x] Build Software & AI, Background/Portfolio, and Contact pages.
- [x] Build the water scheduling project overview with confirmed copy.
- [x] Connect dedicated destinations through shared navigation and homepage links.
- [x] Align all three construction detail pages with the shared design and historical context.
- [x] Expand and group the woodwork gallery; optimize selected images.
- [x] Add page-specific metadata, branded sharing artwork, and an aligned 404 page.
- [x] Expand the software case-study draft using the owner-supplied read-only review, with explicit limits on untested behavior.
- [ ] Confirm remaining case-study details and publication permissions before adding screenshots, customer names, or outcome claims.

### Milestone 3 — Review and release preparation

- [x] Check local links, resource paths, fragments, metadata, email recipients, and image dimensions.
- [x] Check all nine pages return HTTP 200 in the static preview.
- [x] Document release steps and remaining verification in `docs/website-release-checklist.md`.
- [ ] Check desktop/mobile layout, native gallery controls, keyboard navigation, contrast, and reduced-motion behavior in a browser.
- [ ] Confirm final public software copy and material labels with the owner.
- [ ] Confirm the production origin and set absolute sharing/canonical URLs.
- [ ] Verify email drafts in a real mail app; confirm email-only contact is sufficient for launch.
- [ ] Review final local pages with the owner and confirm hosting/deployment access.

Publication remains a separate step. Do not mark release readiness complete while these checks are open.

## 8. Latest validation

Checked nine HTML pages, 238 link/resource references including sharing images, and 36 image elements. No missing resources/fragments, duplicate IDs, duplicate titles, missing metadata/navigation, incorrect email recipients, or image dimension mismatches were found. `git diff --check` passed. Every local page returned HTTP 200, including the preview's direct request for `404.html`; production missing-page routing still needs a host-level check.

Browser inventory reported that the browser access host is unavailable. Desktop/mobile rendering, interactive keyboard behavior, and real email-app handling are unverified. The local preview remains available at `http://localhost:8080/`.
