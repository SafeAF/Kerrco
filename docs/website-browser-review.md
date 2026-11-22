# Desktop browser review handoff

Use this prompt in ChatGPT Desktop with browser access. This review is of the local KERRCO marketing site; no application login is needed.

> Review the static website at `http://localhost:8080/`. If it is unavailable, start a static server from this repository with `web/` as its document root, or ask me to start the existing preview.
>
> Inspect the homepage, Software & AI, Software project, My background, Contact, and all three past construction project pages. Also open `/404.html` to check its recovery links.
>
> Check representative pages at 1440px, 768px, 375px, and 320px wide. Report clipped text, horizontal scrolling, awkward image crops, unreadable text, or overlapping controls. If viewport resizing is unavailable, report which widths you actually checked.
>
> Use keyboard navigation: test the skip link, header/footer links, consultation links, photo links, and native expandable alternate woodwork views. Confirm visible focus and a usable focus order. Open larger photos and use Back to return. Test reduced-motion navigation if available.
>
> Check that software and AI lead the site, the water case study distinguishes observed interface features from untested behavior, and construction is consistently described as past work. Do not infer unsupported features or outcomes.
>
> Inspect email-link recipients, subjects, and the consultation outline without sending a message. If opening an email app is unsupported, record that limit. Do not create production requests, modify application records, publish the site, or change hosting settings.
>
> Return a concise issue list with page URL, viewport, reproduction steps, expected behavior, and a screenshot where useful. Distinguish observed failures from suggestions. If a check passes, record the actual widths or interactions tested. Do not claim full accessibility certification from this review.

The local site's social metadata deliberately points to the confirmed production origin `https://kerrco.us`. A local preview cannot establish that those assets have been deployed there. Production HTTPS, redirects, and real HTTP 404 routing remain host-level release checks.
