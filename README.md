# KERRCO

Software and automation to help small businesses in Twin Falls and the Magic Valley get time back from repetitive manual work and frustrating systems. Samuel Kerr provides custom development, existing-application improvements, integrations, and advice; AI is optional and Linux infrastructure is a supporting service. The public site is static HTML/CSS/JavaScript; a separate Python WSGI endpoint handles inquiry delivery.

The current direction and progress are in [the website rework plan](docs/website-rework-plan.md). See [the release checklist](docs/website-release-checklist.md) for remaining review and hosting steps.

## Site structure

- `web/index.html` — time-savings introduction, actual weather, irrigation, financial, and NetMon application captures, an irrigation case-study thumbnail, software services, and inquiry path. NetMon uses a local synthetic-data fixture. Project tabs support Left/Right and Home/End; all previews remain readable without JavaScript.
- `web/software-ai.html` — software consulting and development, automation, optional AI, and supporting Linux infrastructure.
- `web/workflow.html` — illustrated request-to-estimate walkthrough, other possible projects, and the client process. The optional stage controls use `web/assets/js/workflow.js`; all stages remain readable without JavaScript.
- `web/software-portfolio.html` — Irrigation Water Scheduling, Weather Analysis Suite (IDWX), $CHPY ETF Research Dashboard (ActiveFundPerf), and NetMon Network Monitor, in that order. All four have application captures. The first three have application links; NetMon has two labeled synthetic-data screenshots with full-size links and an inquiry path. See [NetMon capture provenance](docs/netmon-screenshots.md).
- `web/water-delivery-software.html` — water scheduling project overview with order-management and canal flow-history screenshots using test data.
- `web/background.html` — farm, woodwork, and historical construction portfolio.
- `web/contact.html` — short inquiry form, free consultation, email fallback, and project FAQ.
- `web/*-project-details.html` — preserved construction project URLs.
- `web/404.html` — missing-page recovery.
- `web/assets/css/home.css` — shared site styles.
- `web/assets/img/rework/` — optimized photography and sharing artwork; original uploads remain intact elsewhere in the image tree.

The pages are buildless and require no JavaScript for essential content, navigation, or native form submission. The inquiry form posts to `/inquiries`, handled by `server/inquiry.py` through Gunicorn; JavaScript adds inline confirmation and preserves entries on errors. Legacy PHP handlers remain blocked and excluded from releases. See [inquiry setup and delivery checks](docs/inquiry-form.md).

## Local preview

From the repository root:

```sh
python3 server/inquiry.py --port 8091
```

Open `http://127.0.0.1:8091/`. The form validates entries in **preview mode** and explicitly reports that no inquiry was sent. This preview does not execute PHP or configure production routing.

## Deployment

The confirmed production origin is `https://kerrco.us`; canonical and sharing URLs, robots.txt, and sitemap.xml use that origin. The owner selected an Nginx VPS. See [the VPS deployment guide](docs/nginx-deployment.md) and configuration examples in `deploy/nginx/`.

With Node.js and `tar` available, validate and prepare a fresh bundle:

```sh
node scripts/prepare-release.mjs --check
node scripts/prepare-release.test.mjs
node scripts/prepare-release.mjs
```

The script creates a versioned `.tar.gz`, JSON manifest, file-level SHA-256 checksums, and archive checksum in ignored `artifacts/`. It includes only the pages and required static assets. It does not connect to a server. Recreate it after site changes and complete the release checklist before publication. The VPS needs no Node.js runtime. Inquiry delivery requires the separate Python/Gunicorn service, an approved sender, and a working SMTP relay; a static archive alone does not enable the form.

For the remaining visual and keyboard checks, use [the desktop browser-review prompt](docs/website-browser-review.md).

## Inquiry checks

```sh
node scripts/inquiry.test.mjs
python3 -m unittest discover -s server -v
```

The Python suite uses synthetic addresses and a loopback SMTP capture. The production HTTP/SMTP integration test also needs the pinned server dependency:

```sh
python3 -m venv /tmp/kerrco-inquiry-venv
/tmp/kerrco-inquiry-venv/bin/python -m pip install -r server/requirements.txt
KERRCO_GUNICORN=/tmp/kerrco-inquiry-venv/bin/gunicorn python3 -m unittest discover -s server -v
```

No external email is sent by these checks. Actual inbox delivery is a separate deployment check.
