# Desktop browser review handoff

Use this prompt in ChatGPT Desktop with browser access. This review is of the local KERRCO marketing site; no application login is needed.

> Review the static website at `http://127.0.0.1:8091/`. If it is unavailable, run `python3 server/inquiry.py --port 8091` from this repository. This preview explicitly does not send email.
>
> Inspect the homepage, Software Consulting, How it works (`/workflow.html`), Software Portfolio, the water software case study, My background, Contact, and all three past construction project pages. Also open `/404.html` to check its recovery links.
>
> Check representative pages at 1440px, 768px, 375px, and 320px wide. Report clipped text, horizontal scrolling, awkward image crops, unreadable text, or overlapping controls. If viewport resizing is unavailable, report which widths you actually checked.
>
> Use keyboard navigation: test the skip link, header/footer links, consultation links, photo links, and native expandable alternate woodwork views. Confirm visible focus and a usable focus order. Open larger photos and use Back to return. Test reduced-motion navigation if available.
>
> On `/workflow.html`, step through all five stages using the stage buttons and Previous/Next. Test keyboard activation and visible focus, the first/last disabled controls, and the native example disclosures. Visit `/workflow.html#stage-visit` directly, then check that all five stages are readable with JavaScript disabled. The example is fictional and does not send information. Check that the expanded header fits at the tested widths.
>
> Check that software consulting and development lead the site, AI is one possible tool, and infrastructure is secondary. Confirm the water case study distinguishes observed interface features from untested behavior and construction is consistently described as past work. Do not infer unsupported features or outcomes.
>
> On Contact, test required fields, invalid email, optional business, keyboard focus, and submission feedback. Preview must say that no message was sent and must keep entries. Check native submission with JavaScript disabled. Production inbox tests require separate authorization. Inspect email-link recipients and subjects without sending a message. If opening an email app is unsupported, record that limit. Do not create production requests, modify application records, publish the site, or change hosting settings.
>
> Return a concise issue list with page URL, viewport, reproduction steps, expected behavior, and a screenshot where useful. Distinguish observed failures from suggestions. If a check passes, record the actual widths or interactions tested. Do not claim full accessibility certification from this review.

The local site's social metadata deliberately points to the confirmed production origin `https://kerrco.us`. A local preview cannot establish that those assets have been deployed there. Production HTTPS, redirects, and real HTTP 404 routing remain host-level release checks.
