# Homepage evidence deployment — November 25, 2026

Deployed to <https://kerrco.us/> at 9:59 a.m. MST on November 25, 2026 (`2026-11-25T16:59:09Z`), following the owner's explicit “deploy it” request.

The homepage now shows real Weather Analysis and Financial Analytics application screenshots, with weather first and two keyboard-accessible project tabs. The irrigation case study remains available beside them. Opening copy names spreadsheets, repetitive paperwork, and disconnected systems; the header invitation matches the homepage CTA. Public irrigation notes now identify its records as test data.

## Release

- Source: clean local `main`, commit `6c9aa03df613157dca4cdaf72bd46e503119694a`. All 52 packaged public files matched both working-tree bytes and that commit. No commit or push was performed during deployment.
- Host/operator: `proxy-1` (`proxy1`), existing `keystone` identity and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261125T165701Z-6c9aa03-733629f0`, promoted atomically through `/var/www/kerrco/current`.
- Retained predecessor: `/var/www/kerrco/releases/20261125T020025Z-b2a1ea0-b676b789`.
- Archive: `website-review-2026-11-25T16-48-09-583Z-733629f0.tar.gz`.
- Archive SHA-256: `c3121ac4b5db6f99fb74cf11329ecdc1e3c672e87984e710c22fa4f2aba0b19b`.
- Protected evidence: `/var/lib/kerrco-deploy/artifacts/20261125T165701Z-6c9aa03-733629f0`.
- Local evidence: ignored `artifacts/deploy-20261125T165701Z-6c9aa03-733629f0/`.

The 13 changed public files are all 11 HTML pages, `assets/css/home.css`, and `assets/js/software-carousel.js`. Images, backend code, SMTP configuration, and Nginx configuration were unchanged. The earlier demonstration-data batch on `order.kerrco.us` was not rerun or modified by this website deployment.

## Verification

- Local release validation passed for 11 pages, 344 references, 34 image elements, and 52 public files. All seven release-validator tests passed. JavaScript syntax, whitespace, and the project-tab selection/keyboard/fallback checks passed.
- The uploaded archive and all deployment-file hashes matched the local candidate. The server verified the exact predecessor's complete file set and hashes, expected Kerrco Nginx configuration, safe unique archive paths and file types, and every extracted file hash.
- `/var/lib/kerrco-deploy/deploy.lock` was held through promotion and verification. Release directories and files are root-owned with modes 0755 and 0644. The previous release and protected rollback evidence remain available.
- All 52 public HTTPS and all 52 direct-origin HTTPS response hashes, statuses, and MIME types matched the release manifest. TLS certificate and hostname validation remained enabled, including origin requests through loopback using the `kerrco.us` TLS server name.
- Independent workstation requests verified all 52 public file hashes and statuses, the homepage at `/`, both screenshot references, and the weather-first project order.
- The existing inquiry endpoint returned GET 405 with `Allow: POST`, no-store caching, and the expected JSON rejection when JSON was requested. No inquiry was submitted and no email was sent.
- Unknown paths, legacy PHP, dotfiles, and `/inquiries/` returned the custom HTTP 404. HTTP redirected to canonical HTTPS with status 301.
- `nginx -t` passed before and after promotion. All Nginx file hashes, symlink targets, and Nginx/inquiry-service main process IDs were unchanged. No service restart or Nginx reload occurred.
- Weather, Funds, and Water Ordering returned HTTPS 200 before and after promotion. Their deployments and configuration were preserved.
- Temporary remote staging was removed. Local execution records include public/origin responses, independent workstation results, configuration snapshots, and rollback metadata.

Browser inventory again reported that its access host was unavailable. Current rendered appearance, actual browser keyboard/focus behavior, and screen-reader behavior remain unverified; source and Node VM checks do not establish those results. No irrigation screenshot was captured.

## Rollback

Before rollback, require `/var/www/kerrco/current` to resolve to `/var/www/kerrco/releases/20261125T165701Z-6c9aa03-733629f0` and compare Nginx against the protected after-state. Preserve unexpected newer work.

Hold `/var/lib/kerrco-deploy/deploy.lock`. Create a unique sibling symlink pointing to `/var/www/kerrco/releases/20261125T020025Z-b2a1ea0-b676b789`, then atomically replace `current` without dereferencing it. Verify the restored homepage and file hashes, inquiry GET route, HTTPS, redirects, custom 404, and other project sites. No Nginx reload or backend change is required. Exact paths are retained in the protected `rollback.json`.
