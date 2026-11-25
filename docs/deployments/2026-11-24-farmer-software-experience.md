# Farming and software experience wording — November 24, 2026

Published to <https://kerrco.us/> at 7:01 p.m. MST on November 24, 2026 (`2026-11-25T02:01:04Z`), as the owner's requested correction to the live site.

The homepage credibility line now leads with **25 years developing software**. The first-software-job-at-15 detail remains in the fuller background below. The homepage, background page, and contact page explicitly say Samuel currently runs a farm and previously operated a framing company. Background metadata and the farm-gallery introduction reflect that distinction. The full Stanford Linear Accelerator Center name remains.

## Release

- Base commit: `b2a1ea041d2cde96f6d32bc28b7e5ea086c20122`, plus the uncommitted public copy captured in `source.patch`. The cumulative patch includes the preceding Stanford-name correction.
- Source-patch SHA-256: `248bb203ebd67d79917c7b49d87ac758d34b130c3ab0d508bb3a8dcd60d2c141`.
- Active release: `/var/www/kerrco/releases/20261125T020025Z-b2a1ea0-b676b789` on `proxy-1`, using the existing `keystone` deployment identity.
- Retained predecessor: `/var/www/kerrco/releases/20261125T015537Z-b2a1ea0-ddd9a69b`.
- Archive: `website-review-2026-11-25T02-00-25-863Z-b676b789.tar.gz`.
- Archive SHA-256: `834a06166bd3d2db4ab3b02bd39c5bf18546f3dcd131a053ee278bafad792ff7`.
- Protected evidence: `/var/lib/kerrco-deploy/artifacts/20261125T020025Z-b2a1ea0-b676b789`.
- Local evidence: ignored `artifacts/deploy-20261125T020025Z-b2a1ea0-b676b789/`.

Only `index.html`, `background.html`, and `contact.html` differ from the predecessor. Existing uncommitted work was preserved. No commit or push was performed.

## Verification

- Local validation passed for 11 pages, 341 references, 32 images, and 52 release files. Explicit content checks confirmed 25 years in the hero, age 15 below the homepage background heading, and present farming/past framing on all three biography pages. Whitespace checks passed.
- The deployment guarded the exact predecessor, verified its complete file hashes, and checked archive paths, file types, checksums, and extracted hashes before an atomic symlink promotion under the deployment lock.
- All 52 public and origin HTTPS file hashes, statuses, and MIME types matched the manifest. Trusted TLS validation remained enabled.
- Independent workstation checks for all three changed pages matched local source and confirmed the requested wording and placement.
- `nginx -t` passed before and after promotion. Nginx files, symlinks, and service process IDs were unchanged. The inquiry route returned GET 405 with `Allow: POST`; no inquiry or email was sent.
- Redirects, custom 404, PHP/dotfile rejection, and Weather, Funds, and Water Ordering health checks passed. No Nginx reload, service restart, backend, credential, or other project change occurred.
- Remote staging was removed. The previous release and protected rollback evidence remain.

Browser appearance was not rechecked for this wording update.

## Rollback

Guard that `/var/www/kerrco/current` still resolves to this exact active release and Nginx matches the protected after-state. Hold `/var/lib/kerrco-deploy/deploy.lock`, create a unique sibling symlink to the retained predecessor, and atomically replace `current`. Preserve unexpected newer work. Verify the restored homepage, changed pages, inquiry GET route, HTTPS, redirects, and custom 404. No reload or backend change is required. Exact paths are recorded in the protected `rollback.json`.

The predecessor is documented in [the Stanford wording record](2026-11-24-stanford-wording.md).
