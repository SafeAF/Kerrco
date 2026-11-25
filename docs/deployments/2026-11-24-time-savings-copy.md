# Time-savings copy deployment — November 24, 2026

Deployed to <https://kerrco.us/> at 6:51 p.m. MST on November 24, 2026 (`2026-11-25T01:51:35Z`), following Samuel's explicit “deploy it” request.

The site now leads with **Get more time back**, uses Samuel Kerr's full name, brings the Magic Valley construction background forward, and leads the homepage and portfolio with irrigation scheduling. Services, contact, workflow, project descriptions, shared footers, and metadata use the same direction. The contractor example remains fictional, and no measured time-savings claims were added.

## Release

- Source: local `main`, commit `b2a1ea041d2cde96f6d32bc28b7e5ea086c20122`. The working tree was clean before packaging and upload. All packaged bytes matched that commit. No commit or push was performed for deployment.
- Host/operator: `proxy-1` (`proxy1`), existing `keystone` deployment identity and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261125T014909Z-b2a1ea0-237e9eda`, promoted atomically through `/var/www/kerrco/current`.
- Previous release retained: `/var/www/kerrco/releases/20261124T184407Z-14ec54d-1feccd1d`.
- Archive: `website-review-2026-11-25T01-49-09-471Z-237e9eda.tar.gz`.
- Archive SHA-256: `0faaa237060a9ae4863cbf989335061cf3d27c3287f9cc5d949bfd85dc789899`.
- Protected evidence: `/var/lib/kerrco-deploy/artifacts/20261125T014909Z-b2a1ea0-237e9eda`.
- Local evidence: ignored `artifacts/deploy-20261125T014909Z-b2a1ea0-237e9eda/`.

Only the 11 HTML files differ from the predecessor. Styles, JavaScript, images, backend files, SMTP configuration, and Nginx configuration were unchanged. No service restart or Nginx reload was needed.

The standard local release validator supplied the curated 52-file manifest. Its archive subprocess encountered a sandbox `EPERM`; Python's archive writer produced the final bundle from that validated file list. Every staged file was checked against both the manifest and the source commit. The failed local packaging attempt was not uploaded.

## Verification

- Local release validation passed for 11 pages, 341 references, 32 image elements, and 52 public files. All seven release-check tests and all three inquiry-client tests passed.
- Before promotion, the server identity, expected active release, predecessor's complete file set and hashes, Kerrco vhost/snippet hashes, Nginx syntax, and active services matched the recorded baseline.
- The deployment held `/var/lib/kerrco-deploy/deploy.lock` through promotion and verification. The archive checksum, unique safe paths, file types, exact file set, and every extracted hash were verified. Release directories and files are root-owned with modes 0755 and 0644 respectively.
- All 52 public HTTPS responses and all 52 direct-origin HTTPS responses matched the new manifest, expected statuses, and MIME types. Both paths used certificate and hostname validation; origin requests used loopback with the `kerrco.us` TLS server name.
- The homepage at `/` matched the new `index.html`. Independent workstation checks matched all 52 public file hashes and statuses and confirmed the new headline and irrigation-first project order. Results are recorded in `workstation-responses.json` in the local evidence directory.
- The existing `/inquiries` route returned GET 405, `Allow: POST`, no-store caching, and the expected JSON rejection. No inquiry was submitted and no email was sent. This check does not repeat or replace the earlier confirmed inbox-delivery test.
- Unknown paths, legacy PHP, dotfiles, and `/inquiries/` returned the new custom HTTP 404. HTTP redirected to canonical HTTPS with status 301.
- `nginx -t` passed before and after promotion. All Nginx file hashes and symlink targets remained unchanged. Nginx and inquiry-service main process IDs remained unchanged and both services remained active.
- Weather, Funds, and Water Ordering returned HTTPS 200 before and after promotion. Their deployments and configuration were preserved.
- Temporary remote uploads were removed. The previous release and protected evidence remain available.

Browser access was unavailable for this copy rewrite. Current desktop/mobile appearance, interactive keyboard behavior, and screen-reader behavior have not been rechecked. Earlier browser results are recorded in [the consulting refresh deployment](2026-11-24-consulting-refresh.md) and apply to that earlier copy.

## Rollback

Before rollback, verify that `/var/www/kerrco/current` still resolves to `/var/www/kerrco/releases/20261125T014909Z-b2a1ea0-237e9eda` and that Nginx still matches the protected after-state. Preserve any unexpected newer work.

Hold `/var/lib/kerrco-deploy/deploy.lock`. Create a unique temporary symlink beside `current` pointing to `/var/www/kerrco/releases/20261124T184407Z-14ec54d-1feccd1d`, then atomically replace `current` without dereferencing it. Recheck the prior homepage, file hashes, inquiry GET route, HTTPS, redirects, custom 404, and other project sites. No Nginx reload or backend change is required. Exact paths are also recorded in the protected `rollback.json`.
