# Project presentation and flat-fee deployment — November 23, 2026

Deployed to <https://kerrco.us/> at 10:59 a.m. MST on November 23, 2026 (17:59:37 UTC), following the owner's explicit deployment request.

## Release

- Source: `SafeAF/Kerrco`, `main`, commit `e7452a5d542a4ff9eb9aa269bfa0b2cbd3c9d55d`.
- The clean local checkout matched GitHub main before packaging.
- Host/operator: `proxy-1` (`proxy1`), `keystone`, existing deployabot SSH identity and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261123T175834Z-e7452a5-d95a3c57`.
- Active symlink: `/var/www/kerrco/current`.
- Previous release retained: `/var/www/kerrco/releases/20261123T170205Z-b461798-28cb93de`.
- Protected artifacts and evidence: `/var/lib/kerrco-deploy/artifacts/20261123T175834Z-e7452a5-d95a3c57` (root-readable).
- Archive: `website-review-2026-11-23T17-58-34-691Z-d95a3c57.tar.gz`.
- Archive SHA-256: `6111f4989fb264d1b91542e3866b9493f0abe3f289d3a5e27b3cb6711e2d3ffd`.

The homepage carousel and software portfolio now lead with Weather Analysis Suite, followed by $CHPY ETF Research Dashboard and Irrigation Water Scheduling. Related descriptions, project links, and metadata use the descriptive names. The homepage, software offer, workflow, and contact pages emphasize that most projects are flat fee, with scope and price agreed before work begins and any additional work and cost agreed before proceeding.

Activation atomically replaced only the existing document-root symlink after checking its exact predecessor. All previous releases remain. No Nginx configuration, certificate, service, DNS, firewall, or other site's files changed; no reload was needed.

## Verification

- Release validation passed: 11 pages, 346 references, 36 image elements, and 49 packaged files.
- All five release-check tests, both JavaScript syntax checks, and Git whitespace checks passed.
- Archive checksum, exact file list, extracted file hashes, and all 49 public response hashes matched the manifest. The internal `404.html` URL returned HTTP 404 with the expected content.
- Independent workstation HTTPS requests for the homepage, software portfolio, software offer, workflow, and contact pages matched local source byte for byte. The descriptive names, project order, weather-first homepage default, and flat-fee wording were checked in those responses.
- HTTP returned 301 to `https://kerrco.us/`. Trusted TLS hostname verification passed; the existing certificate expires February 11, 2027.
- HTML, CSS, JavaScript, SVG, JPEG, text, and XML MIME types passed for the packaged resources.
- An unknown path, `/forms/contact.php`, and `/.git/config` returned the custom 404 body and HTTP 404.
- `nginx -t` passed before and after activation, Nginx remained active, and existing Nginx file hashes and symlink targets were unchanged.
- Water Ordering, Funds, and Weather returned HTTPS 200 before and after activation.
- Protected evidence includes source and authorization metadata, manifest, checksums, rollback metadata, before/after Nginx hashes and site health, and public-response verification.
- Removed the five temporary upload copies after verification; protected artifacts and all release directories remain.

Visual layout, actual browser/keyboard behavior, screen-reader announcements, and mail-app handling were not tested in this deployment.

## Rollback

Run on `proxy1` through the existing deployment identity. Require the active release to match this record and preserve the new release and protected evidence:

```sh
test "$(readlink -f /var/www/kerrco/current)" = /var/www/kerrco/releases/20261123T175834Z-e7452a5-d95a3c57 &&
test -f /var/www/kerrco/releases/20261123T170205Z-b461798-28cb93de/index.html &&
sudo -n nginx -t &&
sudo -n ln -s /var/www/kerrco/releases/20261123T170205Z-b461798-28cb93de /var/www/kerrco/rollback-20261123T175834Z-e7452a5-d95a3c57 &&
sudo -n mv -T /var/www/kerrco/rollback-20261123T175834Z-e7452a5-d95a3c57 /var/www/kerrco/current
```

Then verify the homepage, assets, redirects, custom 404, and preserved project sites. No Nginx reload is needed for this symlink-only rollback.
