# Fortinet wording deployment — November 24, 2026

Deployed to <https://kerrco.us/> at 11:45 a.m. MST on November 24, 2026 (`2026-11-24T18:45:49Z`), following Samuel's explicit deployment request.

The homepage, background, contact, and software consulting pages now describe later work at Fortinet without specifying its duration. The ten years at SLAC remain. Those four HTML files are the only public changes relative to the previous release.

## Release

- Source: local `main`, commit `14ec54d02e185a19a507e98f380e799a1e42101e`; working tree was clean before packaging. Local main was two commits ahead of its remote-tracking branch. No commit or push was performed for deployment.
- Host/operator: `proxy-1` (`proxy1`), existing `keystone` deployment identity and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261124T184407Z-14ec54d-1feccd1d`, promoted atomically through `/var/www/kerrco/current`.
- Previous release retained: `/var/www/kerrco/releases/20261124T173606Z-16ee369-18a0bed0`.
- Archive: `website-review-2026-11-24T18-44-07-555Z-1feccd1d.tar.gz`.
- Archive SHA-256: `507ab83397bc4f291c90ed6444b5209435325e5bfd72b75bcb0726d27f90407a`.
- Protected evidence: `/var/lib/kerrco-deploy/artifacts/20261124T184407Z-14ec54d-1feccd1d`.

## Verification

- Release validation passed for 11 pages, 341 references, 32 image elements, and 52 public files.
- Archive file set and hashes matched the manifest. The server independently verified that only the four intended HTML files differed from the active predecessor before promotion.
- All 52 public response hashes matched the new manifest; the homepage matched the new `index.html`. The four updated pages contained the revised Fortinet wording without the duration.
- Independent workstation HTTPS requests for all four updated pages matched local source byte for byte and confirmed the revised wording.
- The existing public inquiry route returned GET 405 with `Allow: POST`; no inquiry or email was sent. Nginx and the inquiry service remained active.
- `nginx -t` passed before and after promotion. All Nginx file hashes and symlink targets remained unchanged; no configuration reload or service restart was needed.
- Unknown paths, legacy PHP, and dotfiles returned the expected custom HTTP 404. Weather, Funds, and Water Ordering returned HTTPS 200 before and after promotion.
- Temporary uploads were removed; both releases and protected evidence remain. The preceding browser layout/interaction review is recorded in [the consulting refresh deployment](2026-11-24-consulting-refresh.md); it was not repeated for this text-only change.

## Rollback

Verify the active release still matches this record. Atomically repoint `/var/www/kerrco/current` to `/var/www/kerrco/releases/20261124T173606Z-16ee369-18a0bed0`, using a unique temporary symlink in the same directory. Recheck the homepage, changed pages, and inquiry route. No Nginx reload or backend change is required. Preserve any unexpected newer work instead of overwriting it. Exact paths are also recorded in the protected `rollback.json`.
