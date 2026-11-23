# Software portfolio deployment — November 22, 2026

Deployed <https://kerrco.us/software-portfolio.html> at 5:31 p.m. MST on November 22, 2026 (November 23, 00:31:11 UTC), following the owner's deployment request.

## Release and rollback

- Source: `SafeAF/Kerrco`, `main`, commit `60f66275965b49fbdb478d18367d0cf887673e11`.
- GitHub main matched the clean local checkout before packaging.
- Host/operator: `proxy-1` (`proxy1`), `keystone`, existing deployabot identity and noninteractive sudo.
- Release: `/var/www/kerrco/releases/20261123T003008Z-60f6627-233ab094`.
- Active link: `/var/www/kerrco/current`.
- Retained previous release: `/var/www/kerrco/releases/20261122T235742Z-46db418-a7e6ab0f`.
- Protected artifact and verification record: `/var/lib/kerrco-deploy/artifacts/20261123T003008Z-60f6627-233ab094`.
- Archive: `website-review-2026-11-23T00-30-08-730Z-233ab094.tar.gz`.
- Archive SHA-256: `fc2fe9262fae9fa059aefc157f438c4c753a954a98bc6730251f2ad0c7d6e15f`.

The release adds the Software Portfolio page with Water Ordering, ActiveFundPerf, and IDWX descriptions, features, and application links; renames the navigation throughout the site; and adds related projects to the existing water case study. Only the document-root symlink was switched. No Nginx configuration, certificate, service, DNS, firewall, or other site's files changed, and no reload was needed.

## Verification

- Release validation passed: 10 pages, 293 references, 36 image elements, and 46 packaged files.
- All five release-check tests, JavaScript syntax validation, and Git whitespace checks passed.
- The archive, extracted files, and all 46 public responses matched the release manifest.
- HTTPS, trusted certificate/hostname verification, HTTP-to-HTTPS redirect, CSS/JS/SVG/JPEG MIME types, custom 404 behavior, PHP rejection, and dotfile rejection passed.
- `nginx -t` passed before and after activation; Nginx remained active. Existing Nginx file hashes and symlink targets were unchanged.
- Water Ordering, Funds, and Weather returned HTTPS 200 before and after activation.
- Independent workstation requests matched both the portfolio and homepage source byte for byte. The homepage links to Software Portfolio, and the portfolio contains all three application links.
- Portfolio SHA-256: `b6c7c6f55e5179cf53c18c8fab1e512d760e8433e51f4a98dcea3bfd8cea3634`.
- Temporary upload copies were removed after verification. Protected evidence and the previous release remain.

Browser access was unavailable; visual and interactive browser review was not performed.

## Rollback commands

Run on `proxy1` through the existing deployment identity. Keep the new release and evidence for diagnosis.

```sh
test "$(readlink -f /var/www/kerrco/current)" = /var/www/kerrco/releases/20261123T003008Z-60f6627-233ab094 &&
test -f /var/www/kerrco/releases/20261122T235742Z-46db418-a7e6ab0f/index.html &&
sudo -n nginx -t &&
sudo -n ln -s /var/www/kerrco/releases/20261122T235742Z-46db418-a7e6ab0f /var/www/kerrco/rollback-20261123T003008Z-60f6627-233ab094 &&
sudo -n mv -T /var/www/kerrco/rollback-20261123T003008Z-60f6627-233ab094 /var/www/kerrco/current
```

Then recheck the homepage, assets, redirects, custom 404, and preserved project sites. No reload is needed for this symlink-only rollback.
