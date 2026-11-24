# Consulting refresh deployment — November 24, 2026

Deployed to <https://kerrco.us/> at 10:39 a.m. MST on November 24, 2026 (`2026-11-24T17:39:41Z`), following Samuel's explicit “deploy pls” request. The refreshed contact form is available at <https://kerrco.us/contact.html#inquiry>.

## Release and routing

- Public source: commit `16ee369d2e3f8d5c3026b30ea7e7d892b0931bea` on local `main`. Only nonpublic setup documentation was uncommitted; public source, deployment templates, and backend matched the commit. No commit or push was performed for deployment.
- Host/operator: `proxy-1` (`proxy1`), existing `keystone` deployment identity and noninteractive sudo.
- Active release: `/var/www/kerrco/releases/20261124T173606Z-16ee369-18a0bed0`; `/var/www/kerrco/current` was promoted atomically.
- Previous release retained: `/var/www/kerrco/releases/20261124T004511Z-d479e05-3ea05818`.
- Archive: `website-review-2026-11-24T17-36-06-149Z-18a0bed0.tar.gz`.
- Archive SHA-256: `53030d3e44227fdfad9a8d15bf3eb027dc2f00771f87327cdd0f9400846af2a3`.
- Protected artifacts and evidence: `/var/lib/kerrco-deploy/artifacts/20261124T173606Z-16ee369-18a0bed0`.
- Nginx changes were limited to `/etc/nginx/sites-available/kerrco.us` and new `/etc/nginx/snippets/kerrco-inquiry.conf`. The HTTPS server includes the exact `/inquiries` proxy route to the existing loopback service. A pre-change vhost copy and complete before/after Nginx hashes/symlinks are retained in the protected evidence.
- Deployed vhost SHA-256: `974c584e966f49605aefccf23390da451d4e985dd25b1235e6ac46e1ecedc7e9`. Inquiry snippet SHA-256: `7deea4b9c8f962442167cbbfc572a6e6dec260aa29adfb479d72304db7c35689`.
- The installed inquiry backend, service account, and root-only Gmail configuration were preserved. Samuel had already confirmed receipt of the single authorized test inquiry; no further email was sent.

The public refresh broadens the offer to software consulting and development, retains flat-fee pricing, keeps AI optional and infrastructure secondary, introduces Samuel, and adds authentic weather/CHPY screenshots, a short inquiry form, and project FAQs. Weather remains first, CHPY second, and irrigation scheduling last.

## Technical verification

- Release validation passed for 11 pages, 341 references, 32 image elements, and 52 public files. All seven release-check tests and all three inquiry-client tests passed.
- Archive checksum, exact file set, all extracted hashes, and all 52 public response hashes matched the source manifest. Expected HTML/CSS/JavaScript/JPEG/SVG/text/XML MIME types passed.
- Independent workstation HTTPS requests for the homepage, contact page, and inquiry script matched local source byte for byte.
- Public `/inquiries` returned GET 405 with `Allow: POST` and no-store caching. Invalid JSON and native form requests returned 422; a foreign origin returned 403. These rejected requests never reached SMTP delivery.
- Unknown paths, legacy PHP, dotfiles, and `/inquiries/` returned the expected custom HTTP 404. HTTP redirects to canonical HTTPS.
- `nginx -t` passed before configuration changes, before reload, and after activation. Nginx and the inquiry service remained active. Nginx files and symlinks outside the two intended paths were unchanged.
- Weather, Funds, and Water Ordering returned HTTPS 200 before and after activation. Certificates, DNS, firewall rules, unrelated services, and their vhosts were unchanged.
- Headless Chromium checked the live homepage, services, workflow, portfolio, contact, and background pages at 1440, 768, 375, and 320px: all 24 layout checks passed, visible images loaded, and no horizontal overflow or page JavaScript errors were observed. Desktop homepage and phone contact captures were visually inspected. Intentionally collapsed gallery images were excluded from visible-image assertions; their public bytes were verified in the full manifest check.
- Browser interaction checks passed for carousel order/wraparound, required-field validation, a real public JSON rejection with retained entries and status focus, and native no-JavaScript rejection. The browser constraint was relaxed only in the test DOM to submit a five-character message, which the backend rejects before SMTP. No real inquiry was sent by these checks. Local evidence is under `artifacts/deploy-20261124T173606Z-16ee369-18a0bed0/`; sanitized browser results and the test script are also preserved with the protected deployment evidence.

These checks do not establish a complete accessibility audit, screen-reader announcements, or a separate manual reply test. Successful Gmail delivery was established by the earlier authorized backend test and Samuel's receipt confirmation, rather than another message through the newly public route.

## Rollback

First verify that the active symlink still resolves to this exact release and that Kerrco's vhost/snippet still match the protected after-state. Preserve any unexpected newer work rather than overwriting it.

Atomically restore the retained previous release at `/var/www/kerrco/releases/20261124T004511Z-d479e05-3ea05818`. Restore `/etc/nginx/sites-available/kerrco.us` from the protected `kerrco.us.before.conf` and remove only the unchanged inquiry snippet introduced by this deployment. Run `nginx -t` before reloading; if it fails, retain the working configuration and investigate. Recheck the public homepage, assets, redirects, custom 404, and other project sites. `rollback.json` records the exact paths. All releases and evidence remain available.

The backend may remain running privately after that rollback. Preserve its credential file and source release. Do not disable the backend while the public route remains enabled.
