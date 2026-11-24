# Introduction update deployment — November 23, 2026

Deployed to <https://kerrco.us/> at 5:46 p.m. MST on November 23, 2026 (November 24, 00:46:15 UTC), following the owner's explicit deployment request.

## Release

- Source: `SafeAF/Kerrco`, `main`, commit `d479e051b433830a5751a67885ca5ff855a63f47`.
- The clean local checkout matched GitHub main before packaging.
- Host/operator: `proxy-1` (`proxy1`), `keystone`, existing deployabot SSH identity and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261124T004511Z-d479e05-3ea05818`.
- Active symlink: `/var/www/kerrco/current`.
- Previous release retained: `/var/www/kerrco/releases/20261123T175834Z-e7452a5-d95a3c57`.
- Protected artifacts and evidence: `/var/lib/kerrco-deploy/artifacts/20261124T004511Z-d479e05-3ea05818` (root-readable).
- Archive: `website-review-2026-11-24T00-45-11-934Z-3ea05818.tar.gz`.
- Archive SHA-256: `74fa0ec9303c56fbf8c804171fb79ce2b558be8b528113bdec5fdbf925206162`.

The homepage introduction now leads with a software career beginning at 15. Construction, farming, and woodworking are described as experience that broadened that established software background. Matching copy on the homepage, background, and Software & AI pages follows the same framing.

Activation atomically replaced only the existing document-root symlink after checking its exact predecessor. All previous releases remain. No Nginx configuration, certificate, service, DNS, firewall, or other site's files changed; no reload was needed.

## Verification

- Release validation passed: 11 pages, 346 references, 36 image elements, and 49 packaged files.
- All five release-check tests, both JavaScript syntax checks, and Git whitespace checks passed.
- Archive checksum, exact file list, extracted file hashes, and all 49 public response hashes matched the manifest. The internal `404.html` URL returned HTTP 404 with the expected content.
- Independent workstation HTTPS requests for the homepage, background, and Software & AI pages matched local source byte for byte and contained the revised biography copy.
- HTTP returned 301 to `https://kerrco.us/`. Trusted TLS hostname verification passed; the existing certificate expires February 11, 2027.
- HTML, CSS, JavaScript, SVG, JPEG, text, and XML MIME types passed for the packaged resources.
- An unknown path, `/forms/contact.php`, and `/.git/config` returned the custom 404 body and HTTP 404.
- `nginx -t` passed before and after activation, Nginx remained active, and existing Nginx file hashes and symlink targets were unchanged.
- Water Ordering, Funds, and Weather returned HTTPS 200 before and after activation.
- Protected evidence includes source and authorization metadata, manifest, checksums, rollback metadata, before/after Nginx hashes and site health, and public-response verification.
- The five temporary upload copies were removed after verification; protected artifacts and all release directories remain.

Visual layout, actual browser/keyboard behavior, screen-reader announcements, and mail-app handling were not tested in this deployment.

## Rollback

Run on `proxy1` through the existing deployment identity. Require the active release to match this record and preserve the new release and protected evidence:

```sh
test "$(readlink -f /var/www/kerrco/current)" = /var/www/kerrco/releases/20261124T004511Z-d479e05-3ea05818 &&
test -f /var/www/kerrco/releases/20261123T175834Z-e7452a5-d95a3c57/index.html &&
sudo -n nginx -t &&
sudo -n ln -s /var/www/kerrco/releases/20261123T175834Z-e7452a5-d95a3c57 /var/www/kerrco/rollback-20261124T004511Z-d479e05-3ea05818 &&
sudo -n mv -T /var/www/kerrco/rollback-20261124T004511Z-d479e05-3ea05818 /var/www/kerrco/current
```

Then verify the homepage, assets, redirects, custom 404, and preserved project sites. No Nginx reload is needed for this symlink-only rollback.
