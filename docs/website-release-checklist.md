# Website release checklist

The local site is buildless HTML/CSS in `web/`. The owner selected an Nginx VPS at `https://kerrco.us`. Publication is separate from the local rework. See `nginx-deployment.md` for configuration, upload, verification, and rollback instructions.

## Local review

- [ ] Review `index.html`, `software-ai.html`, `water-delivery-software.html`, `background.html`, and `contact.html` at desktop, tablet, and narrow mobile widths, including 320px. Check for clipped headings, horizontal scrolling, and legible captions.
- [ ] Use Tab and Shift+Tab from the skip link through navigation, consultation links, photo links, and expandable alternate views. Check visible focus, logical order, and Enter/Space activation of the native gallery summaries.
- [ ] Open larger photographs and use browser Back to return. Check all three historical construction pages and their return links.
- [ ] Enable reduced motion and confirm anchor navigation remains usable. Check text/link contrast, including the dark consultation and software panels.
- [ ] Open consultation and software-project links in a real mail app. Check the recipient, subject, and editable consultation outline. Copy the displayed address into webmail as a fallback. Sending a test message is an owner action unless explicitly authorized.
- [ ] Confirm six woodwork material labels and past construction descriptions. Confirm the owner introduction is accurate.
- [ ] Confirm the water application's public access expectations and the final project copy. Add customer names, capabilities, screenshots, or outcome claims only with owner confirmation; screenshots must avoid private operational data.

## Prepare for the existing host

1. The owner confirmed `https://kerrco.us` on an Nginx VPS. Confirm the VPS OS, SSH destination, deployment account, document root, certificate setup, and existing virtual hosts. Configuration templates are in `deploy/nginx/`; they have not been syntax-tested on the VPS.
2. Canonical URLs and absolute sharing-image URLs now use the confirmed origin. Check the deployed site preserves this origin or deliberately revise all metadata if the preferred hostname changes. `404.html` remains excluded from indexing and the sitemap.
3. Back up the currently deployed site using the host's existing backup/release process. Record how to restore that version before replacing files.
4. Run `node scripts/prepare-release.mjs` with Node.js and `tar` available to create a fresh versioned `.tar.gz`, JSON manifest, file-level checksums, and archive checksum in ignored `artifacts/`. The current package contains 43 files with HTML at its root. It excludes original/unreferenced photos, vendor assets, PHP handlers, and repository documents. Preserve originals in the repository. Regenerate after site edits; old ZIP and tar archives are snapshots.
5. Verify the selected release includes all nine HTML pages, `assets/css/home.css`, referenced images, favicon, robots.txt, and sitemap.xml. The current bundle passed checksum and local HTTP checks for all 43 files. No package installation, compilation, database, or PHP execution is required for the current pages.
6. Confirm email-only contact is sufficient. Legacy `forms/*.php` files do not establish working mail delivery and are not connected to the current site. If replacing email links with a form later, test accepted delivery and failures on the actual host before showing success messages.

## Publish and verify

After the owner requests publication, use the VPS upload and versioned-release workflow in `nginx-deployment.md` and preserve the previous release for rollback. Adapt example paths and certificates to the server and pass `nginx -t` before a configuration reload. Do not alter the water application's virtual host.

- [ ] Confirm the homepage and all navigation destinations load over HTTPS.
- [ ] Confirm the three established construction URLs still resolve.
- [ ] Check an unknown URL returns an actual HTTP 404 and serves `404.html`. A direct request for the file in the local static preview only checks its content, not routing.
- [ ] Check absolute sharing image URLs and page titles/descriptions at the production origin.
- [ ] Check the external application link without assuming visitors can sign in.
- [ ] Recheck the email links and mobile layout against deployed assets.
- [ ] Record the release date, deployment method, and rollback reference. If required files fail to load, restore the previous release and investigate before declaring deployment complete.

## Current verification limits

Static checks passed for nine pages, 255 link/resource references, 36 image elements, balanced HTML tags, canonical URLs, sitemap destinations, 404 indexing metadata, and email recipients. The 43-file review archive passed checksum verification, and all 43 local resources returned HTTP 200. Browser automation is unavailable, so visual and keyboard review remains open; use `website-browser-review.md` for the desktop handoff. The water-software case-study draft uses an owner-supplied read-only browser review; evidence and unresolved questions are recorded in `water-delivery-software-review.md`. No publishable screenshots were supplied, and transactional behavior was not tested. No deployment or mail delivery test has been performed.

The repeatable release checker passed against the site. Five automated checks passed, including rejection of missing sharing images, broken stylesheet assets, incorrect canonical URLs, and incomplete sitemaps. A generated tar archive was extracted locally and all 43 file hashes matched its manifest. Nginx is not installed in this local environment; `nginx -t`, TLS, production 404 routing, upload, and rollback still require the VPS.
