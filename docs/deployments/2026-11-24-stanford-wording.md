# Stanford wording correction — November 24, 2026

Published to <https://kerrco.us/> at 6:56 p.m. MST on November 24, 2026 (`2026-11-25T01:56:19Z`), as the owner's requested correction to the just-published site.

The homepage, background page, contact page, and background metadata now spell out **Stanford Linear Accelerator Center**. The established ten years there and later work at Fortinet remain. Strategy notes use the same wording.

## Release and source

- Base commit: `b2a1ea041d2cde96f6d32bc28b7e5ea086c20122` on local `main`, plus the uncommitted three-page wording correction captured in the protected `source.patch`.
- Source-patch SHA-256: `c0c1cbda320e3f1d556159985f60f0770e2b94d06edcc6850ce69877f763fcc8`.
- No commit or push was performed. Existing uncommitted deployment documentation and strategy changes were preserved and excluded from the static archive.
- Host/operator: `proxy-1` (`proxy1`), existing `keystone` deployment account and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261125T015537Z-b2a1ea0-ddd9a69b`.
- Retained predecessor: `/var/www/kerrco/releases/20261125T014909Z-b2a1ea0-237e9eda`.
- Archive: `website-review-2026-11-25T01-55-37-930Z-ddd9a69b.tar.gz`.
- Archive SHA-256: `f06bc3bc9590ebc97b6b9e130354c754d2a8398c08dca7536ca3b64a65965837`.
- Protected evidence: `/var/lib/kerrco-deploy/artifacts/20261125T015537Z-b2a1ea0-ddd9a69b`.
- Local evidence: ignored `artifacts/deploy-20261125T015537Z-b2a1ea0-ddd9a69b/`.

Only `index.html`, `background.html`, and `contact.html` differ from the predecessor. No styles, scripts, images, inquiry backend, credentials, or Nginx configuration changed.

## Verification

- Local validation passed for 11 pages, 341 references, 32 image elements, and 52 release files; whitespace checks passed.
- The server identity, exact predecessor and its complete file hashes, vhost/snippet hashes, and service health were verified before promotion.
- The deployment held the existing deployment lock, verified archive and source-patch hashes, rejected unsafe or duplicate archive paths and links, checked the extracted file set and hashes, and promoted `current` atomically.
- All 52 origin and public HTTPS file hashes, statuses, and MIME types matched the new manifest. Trusted TLS verification remained enabled.
- Independent workstation HTTPS responses for all three changed pages matched local source, contained the full Stanford name, and contained no SLAC acronym.
- `nginx -t` passed before and after promotion. All Nginx file hashes and symlink targets were unchanged. Nginx and inquiry-service main process IDs were unchanged and both services remained active; no reload or restart occurred.
- The inquiry route returned GET 405 with `Allow: POST` and no-store caching. No inquiry or email was sent. HTTP redirects, custom 404, PHP and dotfile rejection, and the three other project sites passed the same checks as the preceding release.
- The previous release and protected rollback record were retained. Temporary remote uploads were removed.

Browser appearance was not rechecked for this wording correction.

## Rollback

Verify that `/var/www/kerrco/current` still resolves to the exact active release above and that Nginx matches the protected after-state. Preserve unexpected newer work. Hold `/var/lib/kerrco-deploy/deploy.lock`, create a unique sibling symlink to the retained predecessor, and atomically replace `current`. Recheck the homepage, changed pages, inquiry GET route, HTTPS, redirects, and custom 404. No Nginx reload or backend change is required. Exact paths are in the protected `rollback.json`.

The preceding release is documented in [the time-savings deployment record](2026-11-24-time-savings-copy.md).
