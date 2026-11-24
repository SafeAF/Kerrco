# Software consulting refresh — November 24, 2026

Scope: local implementation of the owner's requested improvements. Deployment, mail delivery enablement, and new account setup are separate actions.

## Implemented

- Client-focused homepage introduction with the software career retained as a concise credibility line.
- Software consultation, development, existing-application work, automation, and technical advice as the main offer. AI is one option. Linux infrastructure is a supporting section, based on the owner's decades of running Linux servers and services.
- Most projects use a flat fee, with scope and price agreed up front.
- Compact personal-background section on the homepage; complete galleries remain on the existing background page. Existing home fragment IDs and historical project URLs are retained.
- Software Consulting navigation and consultation language throughout the site.
- Project descriptions organized around the challenge, implementation, and usable capability. Weather remains first, CHPY second, and irrigation scheduling last.
- Samuel's name in the introduction, background, and contact page; the confirmed Gmail address remains public.
- Authentic screenshots of the public weather explorer and CHPY research dashboard in the portfolio, with capture dates and direct links. No private irrigation screens were captured.
- Short inquiry form, visible email fallback, and FAQ covering scope, price changes, investigation/prototypes, ownership, hosting, and support.
- Separate WSGI backend, production service/route templates, and local preview with explicit no-send behavior.
- Larger navigation and label text, responsive form layout, visible focus, native field validation, and accessible submission feedback.

## Local verification

- Site checker passed for 11 pages, 341 references, 32 image elements, and 52 public release files.
- The release-check suite and all three inquiry client tests passed.
- The 17-test Python suite passed, including actual Gunicorn HTTP requests and loopback SMTP capture for native and JSON submissions. Synthetic `.test` messages remained local.
- All 11 pages served by the local preview matched source. Native and JSON preview submissions explicitly reported that no inquiry was sent.
- HTML structure, unique IDs, label/ARIA targets, JavaScript syntax, and whitespace checks passed.
- With explicit owner permission, headless Chromium checked the homepage, services, workflow, portfolio, contact, and background pages at 1440, 768, 375, and 320px: no horizontal overflow, broken images, or page JavaScript errors. Desktop and phone captures were visually inspected.
- Browser interaction checks passed for carousel order/wraparound, required-field validation, preview feedback with retained entries and restored button state, status focus, FAQ keyboard activation, the skip link, and native no-JavaScript submission. All submissions stayed in no-send preview mode.

## Outstanding inputs and verification

- Gmail SMTP is selected and its nonsecret settings are in the environment template. Samuel still needs to create a dedicated app password privately. Production configuration and an owner-inbox receipt test remain required before enabling live submissions. See [inquiry delivery](inquiry-form.md).
- No portrait has been supplied; the homepage uses the existing workshop photograph.
- The standard browser tool's access host was unavailable; the owner authorized headless Chromium. The checks above establish the tested layouts and interactions, not a complete accessibility audit. Screen-reader announcements, full keyboard traversal, mail-app behavior, and production HTTPS/routing are not established by the local checks.

Do not describe local preview acknowledgements or captured `.test` mail as real inbox delivery. Do not deploy the static form page without the backend, route, and approved delivery setup ready.
