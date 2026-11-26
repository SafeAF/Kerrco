# Website release checklist

The local site is buildless HTML/CSS in `web/`. The owner selected an Nginx VPS at `https://kerrco.us`. Publication is separate from the local rework. See `nginx-deployment.md` for configuration, upload, verification, and rollback instructions.

## November 24 consulting refresh

The refresh broadens the offer to software consulting and adds a real inquiry endpoint. It was deployed after Samuel confirmed receipt of the authorized Gmail test inquiry; see [the deployment record](deployments/2026-11-24-consulting-refresh.md), [implementation record](2026-11-24-consulting-refresh.md), and [form setup](inquiry-form.md). A static archive alone cannot enable the form. Future releases must preserve the verified backend, SMTP configuration, and exact same-origin route, and check native/enhanced submissions, errors, and the email fallback.

## Local review

- [ ] Review `index.html`, `software-ai.html`, `workflow.html`, `software-portfolio.html`, `water-delivery-software.html`, `background.html`, and `contact.html` at desktop, tablet, and narrow mobile widths, including 320px. Check for clipped headings, horizontal scrolling, and legible captions.
- [ ] Use Tab and Shift+Tab from the skip link through navigation, consultation links, photo links, and expandable alternate views. Check visible focus, logical order, and Enter/Space activation of the native gallery summaries.
- [ ] Open larger photographs and use browser Back to return. Check all three historical construction pages and their return links.
- [ ] Enable reduced motion and confirm anchor navigation remains usable. Check text/link contrast, including the dark consultation and software panels.
- [ ] Open consultation and software-project links in a real mail app. Check the recipient, subject, and editable consultation outline. Copy the displayed address into webmail as a fallback. Sending a test message is an owner action unless explicitly authorized.
- [ ] Confirm six woodwork material labels and past construction descriptions. Confirm the owner introduction is accurate.
- [ ] Confirm the water application's public access expectations and the final project copy. Add customer names, capabilities, screenshots, or outcome claims only with owner confirmation; screenshots must avoid private operational data.

- [ ] On `workflow.html`, use every stage button and Previous/Next with keyboard and pointer. Check boundary controls, the status announcement, native example disclosures, direct links such as `#stage-visit`, and reading all stages with JavaScript disabled. Confirm the five-link header fits desktop and mobile layouts.

## Prepare for the existing host

1. The owner confirmed `https://kerrco.us` on an Nginx VPS. Confirm the VPS OS, SSH destination, deployment account, document root, certificate setup, and existing virtual hosts. Configuration templates are in `deploy/nginx/`; they have not been syntax-tested on the VPS.
2. Canonical URLs and absolute sharing-image URLs now use the confirmed origin. Check the deployed site preserves this origin or deliberately revise all metadata if the preferred hostname changes. `404.html` remains excluded from indexing and the sitemap.
3. Back up the currently deployed site using the host's existing backup/release process. Record how to restore that version before replacing files.
4. Run `node scripts/prepare-release.mjs` with Node.js and `tar` available to create a fresh versioned `.tar.gz`, JSON manifest, file-level checksums, and archive checksum in ignored `artifacts/`. The November 23 workflow-page bundle contains 49 files with HTML at its root. It excludes original/unreferenced photos, vendor assets, PHP handlers, and repository documents. Preserve originals in the repository. Regenerate after site edits; old ZIP and tar archives are snapshots.
5. Verify the selected release includes all 11 HTML pages, the shared and page-specific stylesheets, `assets/js/software-carousel.js`, `assets/js/workflow.js`, `assets/js/inquiry.js`, referenced images, favicon, robots.txt, and sitemap.xml. The irrigation screenshot release has 54 public files, including both irrigation JPEG captures. Static pages need no compilation, database, or PHP; the separate inquiry service needs its pinned Python dependency.
6. Follow [the inquiry setup](inquiry-form.md): privately configure Gmail authentication, install the backend and exact Nginx route, and verify inbox delivery and failures before publishing the refreshed form page. Keep the Gmail email fallback. Legacy `forms/*.php` handlers are not connected to the current site.

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

### November 23, 2026 — workflow page

Added `workflow.html` with a fictional five-stage contractor intake walkthrough, three additional possible workflows, an illustrative AI summary, and the four-step project process. All 11 pages link to it through the shared header and footer. The homepage, software offer, contact, software portfolio, and water case study also include contextual links. Added the canonical URL, sharing metadata, and sitemap destination.

`node scripts/prepare-release.mjs --check` passed for 11 pages, 346 references, 36 image elements, and 49 release files. `node scripts/prepare-release.test.mjs` passed all five checks. JavaScript syntax, balanced HTML, control targets, shared navigation, and whitespace checks passed. A Node DOM fixture checked all stage selections, Previous/Next boundaries and focus handling, fragment selection, hash changes, and the incomplete-markup fallback. The source HTML exposes all five stages when JavaScript is unavailable. These checks do not establish browser rendering or keyboard behavior.

The browser inventory reported that its access host is unavailable. Desktop/mobile layout, actual focus rendering, screen-reader announcements, and browser behavior remain open for review using `website-browser-review.md`. No deployment or mail delivery test was performed.

Local review bundle: `artifacts/website-review-2026-11-23T16-41-04-166Z-6c1f47ed.tar.gz`, with the matching JSON manifest, file checksums, and archive checksum. The sandbox blocked the release script's Node `tar` subprocess with `EPERM` after staging. Python's standard-library `tarfile` packaged that staged content instead; the archive's exact file list and all 49 content hashes matched the manifest, and its SHA-256 sidecar was verified. This bundle is a local snapshot, not a deployed release.

### Earlier verification snapshots

Static checks passed for nine pages, 255 link/resource references, 36 image elements, balanced HTML tags, canonical URLs, sitemap destinations, 404 indexing metadata, and email recipients. The 43-file review archive passed checksum verification, and all 43 local resources returned HTTP 200. Browser automation is unavailable, so visual and keyboard review remains open; use `website-browser-review.md` for the desktop handoff. The water-software case-study draft uses an owner-supplied read-only browser review; evidence and unresolved questions are recorded in `water-delivery-software-review.md`. No publishable screenshots were supplied, and transactional behavior was not tested. No deployment or mail delivery test has been performed.

The repeatable release checker passed against the site. Five automated checks passed, including rejection of missing sharing images, broken stylesheet assets, incorrect canonical URLs, and incomplete sitemaps. A generated tar archive was extracted locally and all 43 file hashes matched its manifest. Nginx is not installed in this local environment; `nginx -t`, TLS, production 404 routing, upload, and rollback still require the VPS.
