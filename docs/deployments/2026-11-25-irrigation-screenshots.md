# Irrigation screenshots deployment — November 25, 2026

Published to <https://kerrco.us/> at 5:26:51 PM MST on November 25, 2026 (`2026-11-26T00:26:51.470324+00:00`), completing the owner's request for the missing irrigation application pictures.

## Visible result

The homepage includes an Irrigation Scheduling project tab between Weather Analysis and Financial Analytics, plus a linked irrigation thumbnail that stays visible with every tab. Weather remains the initial project. The portfolio includes the current-order screenshot. The [irrigation case study](https://kerrco.us/water-delivery-software.html#screenshots) shows the current-order table and canal flow-history chart, each with a text description and a full-size image link.

The images are actual rendered application captures, labeled as test data and dated November 25, 2026. No interface values or labels were fabricated or altered. Browser framing selects the current-order table and the full canal chart. The owner explicitly authorized headless Chromium after the normal browser connection remained unavailable. Capture used the application's publicly displayed demo login; no order, approval, rejection, or application setting was changed.

- `assets/img/rework/irrigation-orders-screen.jpg`: 1440 × 700, SHA-256 `9371515440f7327dbdd6552657d5682582dae2227171a240bad084f99045a1ef`.
- `assets/img/rework/irrigation-canal-screen.jpg`: 1440 × 1100, SHA-256 `bf65f5b21422a80348dbf7983f8aebc82f2642b331c6f4e516b8167f2e6e237d`.

## Release

- Source base: `6c9aa03df613157dca4cdaf72bd46e503119694a`, plus the exact text/binary changes captured in protected `source.patch`. The patch includes the two new JPEGs. Reconstructing the base plus patch in a fresh temporary tree reproduced all 54 public file hashes. Existing workspace documentation was preserved. No commit or push was performed.
- Source-patch SHA-256: `b2aebadd504190df7796efb76c0a2d3248f029545bea4bf33da69b4794480068`.
- Host/operator: `proxy-1` (`proxy1`), existing `keystone` identity and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261126T002551Z-6c9aa03-0a052edd`, promoted atomically through `/var/www/kerrco/current`.
- Retained predecessor: `/var/www/kerrco/releases/20261125T165701Z-6c9aa03-733629f0`.
- Archive: `website-review-2026-11-26T00-25-51-657Z-0a052edd.tar.gz`.
- Archive SHA-256: `3b92831f940b255fd33e25e5f5f84632eb699014442e46e9ea0293e34209ef0e`.
- Protected evidence: `/var/lib/kerrco-deploy/artifacts/20261126T002551Z-6c9aa03-0a052edd`.
- Local evidence: ignored `artifacts/deploy-20261126T002551Z-6c9aa03-0a052edd/`; capture provenance and browser review are under `artifacts/irrigation-captures-2026-11-25/`.

Four existing public files changed: `index.html`, `software-portfolio.html`, `water-delivery-software.html`, and `assets/css/home.css`. The two JPEGs are the only added public files. JavaScript, backend code, SMTP configuration, Nginx configuration, and application data were preserved.

## Verification

- Local release validation passed for 11 pages, 356 references, 39 image elements, and 54 public files. All seven release-validator tests, JavaScript syntax, and whitespace checks passed.
- Owner-authorized headless Chromium checked the three affected pages at 1440, 768, 375, and 320px: all visible images decoded, no horizontal overflow, and no page JavaScript errors. Project selection, Left/Right wraparound, Home/End, focus moving into the active panel, all three no-JavaScript project panels, and thumbnail/full-size navigation passed. Desktop and phone captures were visually reviewed.
- The server held `/var/lib/kerrco-deploy/deploy.lock`, verified the exact predecessor's complete file set and hashes, checked archive paths/types/checksums, and verified every extracted file before promotion. It required exactly the four changed files and two added JPEGs.
- All 54 public HTTPS and all 54 direct-origin HTTPS file hashes, statuses, and MIME types matched the manifest. TLS certificate and hostname verification remained enabled.
- Independent workstation checks verified all six changed/added files. Live headless checks of the three affected pages at 1440 and 375px confirmed the irrigation images loaded and no horizontal overflow. The homepage still selected Weather Analysis first, and the new Irrigation Scheduling tab displayed its screenshot.
- The inquiry route returned GET 405 with `Allow: POST`; no inquiry or email was sent. HTTP redirects and custom 404/PHP/dotfile rejection passed.
- `nginx -t` passed before and after promotion. Nginx files, symlinks, and Nginx/inquiry-service main process IDs were unchanged. No reload or restart occurred. Weather, Funds, and Water Ordering returned HTTPS 200 before and after promotion.
- Remote staging was removed; the prior release and protected rollback evidence remain available.

These browser checks establish the tested layouts and interactions, not full accessibility certification or physical water-delivery behavior.

## Rollback

Require `/var/www/kerrco/current` to resolve to `/var/www/kerrco/releases/20261126T002551Z-6c9aa03-0a052edd` and compare Nginx against the protected after-state. Preserve unexpected newer work. Hold `/var/lib/kerrco-deploy/deploy.lock`, create a unique sibling symlink pointing to `/var/www/kerrco/releases/20261125T165701Z-6c9aa03-733629f0`, and atomically replace `current`. Verify the restored homepage/file hashes, inquiry GET route, HTTPS, redirects, custom 404, and other project sites. No reload or backend change is required. Exact paths are recorded in protected `rollback.json`.
