# KERRCO website rework plan

Date: November 2, 2026  
Status: Ready for implementation; discovery complete  
Scope: Rework the existing static site in `web/`, review locally, then prepare for the existing hosting environment.

## 1. Direction

Present KERRCO as one business with three clear areas of work:

1. **Construction** — residential and commercial construction work, supported by the existing project portfolio.
2. **Woodwork** — handmade bowls, vessels, and other wood pieces, supported by the actual photos in `web/assets/img/woodwork/`.
3. **Software & AI** — custom business software, workflow automation, and practical AI consulting for small businesses, with a free initial consultation.

The shared story is hands-on problem solving: building useful things, understanding how work happens, and paying attention to the details. Each area gets its own explanation, proof, and next step so visitors can quickly find what they need.

Keep the KERRCO name and the construction company's local identity. Use the owner’s construction and making background to explain the software consulting perspective. Do not imply separate companies or a large consulting team.

### Changes from the previous plans

This document is the implementation direction for this rework. Retain `docs/REVAMP-PLAN-CODEX.md` and `docs/strategy/local-ai-consulting.md` as background.

- Make **AI consulting explicit and easy to find**. The old instruction to avoid an AI consulting headline does not apply to this direction.
- Keep the older plans' emphasis on specific business problems and practical outcomes.
- Use **Woodwork**, rather than **Architectural Woodwork**, as the main label. The available portfolio shows turned pieces; it does not establish a portfolio of mantels, built-ins, or cabinetry.
- Feature the live water delivery scheduling software as the first software case study.
- Make the free consultation a clear offer with an honest request flow.
- Launch without waiting for the RAG demo. Add it as a second software proof point when ready.

## 2. What is available now

| Asset | Current state | Use in the rework |
| --- | --- | --- |
| Static HTML/CSS/JS site | `web/index.html`, shared styles and scripts | Retain the simple deployment model |
| Construction portfolio | North Temple framing, urgent care remodel, Adell home | Keep existing URLs and project images; improve presentation |
| Woodwork photography | 11 files in `web/assets/img/woodwork/` | Curate a gallery; group multiple views of the same piece |
| Water scheduling software | Live at `https://orders.kerrco.us`, according to the owner | Software case study and appropriate external link |
| Contact email | `kerrcoenterprises@gmail.com` in the current site | Working inquiry route for the first local version |
| PHP mail handlers | Existing contact and quote scripts | Evaluate against actual hosting before using a submitted form |
| RAG demo | Planned; not available yet | Future addition; no active demo button at launch |

The public software URL could not be inspected through the web reader during planning. Feature details, screenshots, customer naming, and public access still need verification; none should be inferred from the older plan.

## 3. Audiences and visitor paths

| Visitor | What they need to see | Next step |
| --- | --- | --- |
| Homeowner, builder, or commercial client | Construction scope, real projects, service area | Discuss a construction project |
| Person interested in handmade woodwork | Clear photos, materials, process, availability information | Ask about a piece or a possible custom project |
| Small business owner | Concrete software/AI use cases, working software proof, understandable process | Request a free consultation |

Construction keeps its local Twin Falls / Magic Valley context. Lead consulting examples with businesses whose work overlaps that experience, such as contractors, service businesses, and irrigation operations. Do not claim nationwide service or specific integrations without confirmation.

## 4. Site structure

Use direct navigation: **Construction · Woodwork · Software & AI · Contact**, with the logo linking home. Include a prominent **Free AI consultation** link to the consulting inquiry section.

| Page | Purpose and required content |
| --- | --- |
| `index.html` | Introduce all three areas, show selected work, explain the shared approach, direct each audience onward |
| `construction.html` | Construction services, existing projects, local context, project inquiry CTA |
| `woodwork.html` | Curated gallery, materials and making process where known, inquiry CTA |
| `software-ai.html` | Consulting offer, business problems addressed, water software proof, free consultation process |
| `water-delivery-software.html` | Verified case study explaining the scheduling problem and the software built |
| `contact.html` | Clear inquiry choices, email contact, consultation request instructions |
| Existing three construction detail pages | Preserve URLs; align navigation, typography, and inquiry links with the new site |

Put a short About section on the homepage initially. A separate About page, a general Services page, and a combined Projects page can wait until they add useful content beyond these pages.

## 5. Homepage content and layout

### Header and hero

Suggested headline:

> Construction. Woodwork. Practical software.

Suggested supporting copy:

> KERRCO brings hands-on building experience to construction, handcrafted woodwork, and software and AI tools for small businesses. Based in Twin Falls, Idaho.

Primary action: **Explore the work**. Secondary action: **Free AI consultation**.

Use a strong real project photograph with readable text and a nearby three-part image composition or preview strip. Make construction, woodwork, and software visible near the top of the page; avoid relying on a rotating hero to communicate the three areas.

### Three clear paths

Each area gets a real image, a short explanation, and a descriptive link:

- **Construction:** Framing, remodeling, and finish work, with the existing portfolio as evidence. Link: **View construction work**.
- **Woodwork:** Handmade wood pieces that show the grain, shape, and character of the material. Link: **Explore the woodwork**.
- **Software & AI:** Custom software and practical AI help for scheduling, paperwork, and everyday business workflows. Link: **Explore software & AI**.

Treat construction service lists already on the site as draft content to review for current scope, rather than expanding them with unsupported capabilities.

### Selected work

Show one construction project, a small group of standout wood pieces, and the water delivery software case study. Use visible titles and captions, with links usable on touchscreens. More photos of the same bowl should appear inside its gallery rather than as separate projects.

### Free consultation feature

Suggested headline:

> Find a useful place to start with AI.

Suggested copy:

> Have a repetitive office task, a scheduling headache, or information that is hard to find? Start with a free consultation. We’ll talk through how your business works and where software, automation, or AI could help.

CTA: **Request a free consultation**.

### About and contact

Explain the connection between construction, craftsmanship, and software in a short owner-led introduction. Close with distinct links for construction, woodwork, and software inquiries, plus the existing email address.

## 6. Construction page

- Lead with construction photography and the Twin Falls / Magic Valley service context.
- Explain current service scope in clear language, using the existing framing, remodel, and finish work content as a starting point.
- Feature the three existing project pages, with accurate descriptions of KERRCO's role.
- Keep construction inquiry wording focused on the project, location, and rough timeline.
- Confirm current license/insurance wording before carrying it into new public copy; the existing site contains those claims.
- Preserve established project URLs and update navigation to work from every detail page.

## 7. Woodwork page and image preparation

Start with the actual portfolio: walnut, apricot, and birch pieces identified by the existing filenames. Verify labels against the owner's knowledge before final publication.

Initial image groups:

- Walnut bowls, including the three `walnut-bowl-7.5-deep-*` views.
- Apricot bowl, process image, and serving piece.
- Spalted birch bowl/cup and the other birch piece.

Implementation requirements:

- Review all 11 files before final selection; check which files depict the same object.
- Give the extensionless `apricot-serving-tray-platterjpeg` asset a correctly named web copy after checking its actual format. Preserve the original.
- Use consistent gallery thumbnails and larger images that preserve each piece's shape.
- Create optimized web derivatives where useful; keep originals intact and avoid upscaling small photos.
- Add descriptive alt text, image dimensions, and lazy loading below the first screen.
- Use short captions for verified material, form, and process. Do not derive dimensions or food-safety claims from filenames or photographs.
- Use **Ask about this piece** as the initial CTA. Describe commissions, prices, shipping, and availability only after those policies are confirmed.

Launch as a portfolio and inquiry page. An online store is outside this first rework.

## 8. Software & AI consulting page

Suggested headline:

> Software and AI that help your business get work done.

Explain the offer in three parts:

1. **Find the opportunity:** Understand the workflow, repetitive work, and places where information gets lost.
2. **Choose a practical approach:** Consider existing software, integrations, automation, custom software, or AI based on the problem.
3. **Build and support the solution:** Define a focused scope, try it in the real workflow, and help people use it.

Use concrete examples as possible projects, not claims about completed client work:

- Scheduling and order tracking.
- Reducing duplicate entry between forms, spreadsheets, and business tools.
- Organizing customer requests and follow-up work.
- Preparing draft summaries or reports for staff review.
- Making business documents easier to search.
- Building a focused internal tool when existing products do not fit.

Explain when AI is useful and when a simpler software change may be enough. Keep technical terminology secondary to the business task.

### Free consultation offer

- The initial conversation is free.
- Ask about the business, the workflow causing trouble, and what a useful improvement would look like.
- Explain that the next step may be a recommendation or a separately scoped project.
- Do not promise a free implementation, a specific call duration, fixed savings, or instant calendar booking.
- Use **Request a free consultation** until a scheduling system is actually available.

### Water delivery software case study

Use the owner's confirmed description: **water delivery scheduling software**.

Build the story around:

- The real workflow and the problem it needed to solve.
- What KERRCO built and the owner's actual role.
- Verified capabilities and selected screenshots.
- How the system is used today.
- Outcomes only where there is supporting evidence; qualitative outcomes are acceptable.

Link to `https://orders.kerrco.us` with wording that matches its access model. A production login page should be labeled as the live application, not advertised as an open demo. Keep the case study useful even if visitors cannot sign in. Use sanitized screenshots or demo data if operational information would otherwise appear.

Do not assert customer names, headgate tracking, reporting features, usage numbers, or time savings just because they appeared in an earlier plan.

### Future RAG demonstration

Reserve a place in the page structure for a business document search demo. Do not show a disabled button or empty placeholder to visitors in the first release.

When ready, introduce it in plain language, such as **Ask questions about your business documents**. A useful demo should show an example question, an answer with supporting source references, and what happens when the supplied documents do not contain an answer. Use public or synthetic demonstration documents.

The water scheduling software and the RAG demo should become two different examples of the work: operational software and AI-assisted knowledge retrieval.

## 9. Inquiry flow

The first local version should use the existing email address with contextual subjects for construction, woodwork, and free consultation requests. Always display the email address so visitors can copy it. Email links should clearly open the visitor's mail app and must not show a false submission-success message.

Before launch, decide whether email-only contact is sufficient or connect a tested form to a supported delivery service. The current Python static preview does not execute PHP; existing PHP files do not establish that the production host can deliver mail.

If a submitted form is added, keep it short:

- Name.
- Email.
- Inquiry type: Construction / Woodwork / Software & AI.
- Business name, optional.
- Short description of the project or workflow.

Use separate intent labels such as **Discuss a construction project**, **Ask about woodwork**, and **Request a free consultation**. Only show success after the configured endpoint accepts the request; provide an email fallback on failure.

## 10. Visual and technical approach

- Keep the KERRCO wordmark; use charcoal/navy, warm off-white, and a restrained gold accent.
- Let real construction and woodwork photos supply texture and character. Use real application screenshots when available.
- Use a consistent layout, typography, and navigation across the three areas. Give woodworking photos enough space to show the objects clearly.
- Replace the current generic welcome and full-screen carousel with a concise introduction and clear paths into the work.
- Keep text readable on images, visible keyboard focus, accessible navigation, and comfortable mobile targets.
- Avoid essential content that depends on animation, hover, or a JavaScript preloader.
- Retain static HTML/CSS/JS and the current `web/` deployment root. Do not introduce a framework or CMS for this scope.
- Keep Bootstrap or existing gallery tools where useful; remove unused dependencies only after the new pages no longer need them.
- Set page-specific titles, descriptions, and sharing metadata. Keep location-specific construction language on the construction pages and clear software/AI consulting language on the consulting page.

## 11. Implementation sequence

### Milestone 1 — Working homepage for local review

- [x] Review existing plans, site structure, contact scripts, and image inventory.
- [x] Inspect representative woodwork photos and identify positioning changes.
- [x] Write this implementation plan.
- [x] Select homepage photography and prepare initial image derivatives.
- [x] Rework the homepage header, hero, three service paths, selected work, consultation offer, About section, and footer.
- [x] Make all inquiry actions work through the existing email address.
- [x] Keep links within the homepage or to existing pages until the new destination pages exist.
- [ ] Review the first version locally on desktop and mobile widths.

**Exit condition:** The homepage represents all three areas with real evidence, has working next steps, and can be reviewed at the local preview without waiting for the RAG demo or new screenshots.

### Milestone 2 — Complete the portfolio and consulting paths

- [ ] Build Construction, Woodwork, Software & AI, and Contact pages.
- [ ] Build the water delivery software case study with verified copy and available approved visuals.
- [ ] Align the three existing construction detail pages with the shared design.
- [ ] Finish woodwork grouping, captions, gallery behavior, and image optimization.
- [ ] Replace temporary homepage anchor destinations with the completed page links.
- [ ] Add final page metadata and sharing images.

**Exit condition:** Each audience has a complete route from the homepage through relevant proof to a clear inquiry action.

### Milestone 3 — Verify and prepare for release

- [ ] Check links, image paths, gallery controls, and cross-page navigation.
- [ ] Check desktop and mobile rendering, keyboard use, contrast, and reduced-motion behavior.
- [ ] Confirm current construction service scope and business claims.
- [ ] Confirm public-facing software details, screenshots, and link labeling.
- [ ] Verify email links; if a form is included, test delivery and failure handling on the actual supported host.
- [ ] Check image sizes and remove unused page dependencies where appropriate.
- [ ] Review the final local site with the owner and document deployment steps for the existing host.

**Exit condition:** The site is ready for the existing hosting environment, with any verification limits recorded. Publication is a separate step from this local rework.

### Milestone 4 — Add the RAG demo when ready

- [ ] Add a dedicated demo or case-study page with representative questions and source references.
- [ ] Link it from Software & AI and, if it strengthens the introduction, the homepage.
- [ ] Keep demonstrations distinct from production customer data and verified client outcomes.

## 12. Details to confirm during implementation

These do not block the first homepage build:

- Current construction service scope and any license/insurance wording.
- Whether woodwork inquiries should emphasize existing pieces, commissions, or both.
- Preferred public owner introduction and whether a portrait/workshop photo is available.
- Public case-study details, customer naming permission, screenshots, and access expectations for the water scheduling application.
- Whether remote software consulting should be advertised alongside the local business focus.
- Production hosting capabilities and whether to use email-only contact or a delivered form.

Default working assumptions: keep the existing public email, maintain local construction positioning, show woodwork as a portfolio with inquiries, state the free consultation offer plainly, and keep the RAG demo out of the launch requirements.

## 13. Implementation notes — November 2, 2026

Milestone 1 source work is implemented in `web/index.html` and `web/assets/css/home.css`. The homepage uses section destinations for Construction, Woodwork, Software & AI, consultation, and contact. The existing `services`, `projects`, and `footer` anchors remain available for links from the construction detail pages. Those detail pages and their shared styles/scripts are unchanged.

- Replaced the carousel and template dependencies on the homepage with a static, responsive layout. Essential content and navigation require no JavaScript. Included a skip link, visible keyboard focus, reduced-motion styling, and native expandable alternate photography.
- Reviewed all 11 woodwork files in a contact sheet. Selected `walnut-bowl.jpeg` and `spalted-birch-bowl.jpeg` for the homepage; grouped `walnut-bowl2.jpeg` as an alternate view rather than a separate project. The three `walnut-bowl-7.5-deep-*` photos remain grouped for the later gallery. Final material labels and other piece relationships still need owner review.
- Added JPEG web derivatives in `web/assets/img/rework/`, preserving originals and avoiding upscaling. Checked the extensionless apricot serving-piece original as JPEG and created `apricot-serving-tray-platter.jpg` for the later gallery. The homepage's four unique image files total about 446 KiB.
- Inquiry links use the existing email with contextual subjects. The consultation link also supplies a short editable email outline. No submitted form, calendar booking, or success message is included.
- The water scheduling feature uses only the owner-confirmed description and labels the external destination as a live application. Its access model, screenshots, and fuller case study remain unverified.
- Validation: local homepage returned HTTP 200; checked all 39 homepage link/resource references, section destinations, construction-page return anchors, a single H1, and alt text/dimensions on all seven image elements. `git diff --check` passed.
- Desktop/mobile visual review and interactive keyboard checks remain open: the browser automation host was unavailable. The existing preview at `http://localhost:8080/` serves the updated homepage. Email URL checks establish the intended recipient and subject; opening a visitor's mail app and sending mail were not tested.

Next: complete the local visual review, then begin Milestone 2's dedicated pages. No publication or hosting changes have been made.
