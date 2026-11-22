# KERRCO

Static website for practical software, automation, and AI consulting, supported by a portfolio of hands-on experience in farming, woodworking, and past construction work.

The current direction and progress are in [the website rework plan](docs/website-rework-plan.md). See [the release checklist](docs/website-release-checklist.md) for remaining review and hosting steps.

## Site structure

- `web/index.html` — software-led homepage.
- `web/software-ai.html` — consulting offer and possible project types.
- `web/water-delivery-software.html` — water scheduling project overview.
- `web/background.html` — farm, woodwork, and historical construction portfolio.
- `web/contact.html` — free consultation and software inquiry instructions.
- `web/*-project-details.html` — preserved construction project URLs.
- `web/404.html` — missing-page recovery.
- `web/assets/css/home.css` — shared site styles.
- `web/assets/img/rework/` — optimized photography and sharing artwork; original uploads remain intact elsewhere in the image tree.

The pages are buildless and require no JavaScript for essential content or navigation. Older template/vendor files and PHP handlers remain in the repository but are not loaded or submitted to by the current pages. Contact uses email links rather than a submitted form.

## Local preview

From the repository root:

```sh
python3 -m http.server 8080 --directory web
```

Open `http://localhost:8080/`. This static preview does not execute PHP or configure production missing-page routing.

## Deployment

The confirmed production origin is `https://kerrco.us`; canonical and sharing URLs, robots.txt, and sitemap.xml use that origin. The owner selected an Nginx VPS. See [the VPS deployment guide](docs/nginx-deployment.md) and configuration examples in `deploy/nginx/`.

With Node.js and `tar` available, validate and prepare a fresh bundle:

```sh
node scripts/prepare-release.mjs --check
node scripts/prepare-release.test.mjs
node scripts/prepare-release.mjs
```

The script creates a versioned `.tar.gz`, JSON manifest, file-level SHA-256 checksums, and archive checksum in ignored `artifacts/`. It includes only the pages and required static assets. It does not connect to a server. Recreate it after site changes and complete the release checklist before publication. The VPS needs no Node.js runtime for the static site.

For the remaining visual and keyboard checks, use [the desktop browser-review prompt](docs/website-browser-review.md).
