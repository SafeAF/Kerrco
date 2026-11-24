# Inquiry form and delivery

The contact page has four visible fields: name, email, optional business, and a short description. It submits to the same-origin `POST /inquiries` endpoint. Native HTML submission works without JavaScript; the enhancement provides inline feedback and keeps entries when submission fails.

The site remains buildless. Inquiry delivery is a separate Python WSGI service behind Nginx, rather than the legacy PHP handler. Nothing in this implementation changes the existing production mail service.

## Delivery status

On November 24, 2026, the committed backend (`16ee369d2e3f8d5c3026b30ea7e7d892b0931bea`) was installed on `proxy-1` as the dedicated `kerrco-inquiry` service. It is enabled and running only on `127.0.0.1:8766`. After Samuel confirmed delivery and requested deployment, the refreshed website and exact public Nginx `/inquiries` route were activated. See [the backend setup record](deployments/2026-11-24-inquiry-backend.md) and [public deployment record](deployments/2026-11-24-consulting-refresh.md).

On November 24, 2026 Mountain time, a read-only host inspection found Exim running on loopback. Its routing test for the existing public recipient returned **“Mailing to remote domains not supported.”** Therefore the current host mail service cannot be used to deliver inquiries to the Gmail inbox without further configuration. Do not enable the live form route on the assumption that local SMTP is sufficient.

Samuel confirmed that `kerrcoenterprises@gmail.com` remains the public contact address and Gmail is the preferred delivery service. `deploy/kerrco-inquiry.env.example` contains Gmail's host, sender, username, STARTTLS, and port 587; its password is intentionally blank. Configure the credential privately in `/etc/kerrco-inquiry.env`, root-owned mode `0600`; never put credentials in repository files, command arguments, screenshots, or chat.

Samuel privately saved the app password in that server file. Google's display spaces were removed without displaying the secret, and Gmail STARTTLS authentication passed. Authentication did not send email. Samuel then explicitly authorized one real test inquiry; the running backend returned HTTP 201 after Gmail SMTP accepted it at `2026-11-24T17:30:57Z`. Samuel subsequently confirmed receipt on November 24, 2026. Public routing and invalid native/JSON submissions were verified during deployment without sending another message. No separate manual reply test is recorded.

## Gmail setup

The current backend supports Gmail's authenticated SMTP using a dedicated app password. It does not implement Google OAuth. Google recommends Google sign-in where available; app passwords are an option for clients without that integration.

1. In the Google account for `kerrcoenterprises@gmail.com`, enable 2-Step Verification if it is not already enabled.
2. Open [Google App Passwords](https://myaccount.google.com/apppasswords) privately and create an entry named `KERRCO inquiry form`. Use this app password for `KERRCO_SMTP_PASSWORD`, rather than the normal account password. Do not send the credential in chat.
3. At deployment, store it directly in the server's root-only environment file using a private editor. Keep the remaining values from the example: sender and SMTP username are the Gmail address, host is `smtp.gmail.com`, port is `587`, and security is `starttls`. No POP or IMAP access is needed for this send-only form.
4. Start the backend and verify one clearly labeled test inquiry reaches the inbox before enabling the public form. The visitor's address is Reply-To; the authenticated Gmail account is the sender and recipient.

Google documents the [SMTP settings](https://support.google.com/mail/answer/7104828?hl=en) and [app-password requirements](https://support.google.com/accounts/answer/185833?hl=en). App passwords may be unavailable with Advanced Protection, security-key-only verification, or some organization accounts. If unavailable, use an OAuth integration or another authenticated delivery provider rather than weakening account security. Changing the Google account password revokes app passwords, so the service credential would need replacing.

## Runtime

- `server/inquiry.py`: WSGI application and local preview.
- `server/requirements.txt`: pinned Gunicorn dependency.
- `server/gunicorn.conf.py`: one worker with four threads, bound only to `127.0.0.1:8766`.
- `deploy/kerrco-inquiry.service`: dedicated service template.
- `deploy/nginx/kerrco-inquiry.conf`: exact `/inquiries` route for the existing `kerrco.us` HTTPS server.

The production factory validates delivery configuration before starting. It supports authenticated STARTTLS or implicit TLS SMTP with certificate verification. Unencrypted SMTP is restricted to loopback. The recipient, sender, and subject come from configuration/code; visitors supply only the reply address and message. No visitor autoresponder is sent.

The endpoint bounds request and field sizes, rejects duplicate/unknown fields and email-header injection, checks the browser origin, and has a honeypot and bounded in-memory IP rate limit. Nginx replaces the trusted client-IP header. Keep the configured single-worker model so the rate-limit state is shared by all serving threads. An SMTP relay should also have its own sending limits.

There is no inquiry database or payload logging. Submitted content is passed to the configured SMTP recipient. SMTP acceptance is required for a successful response; it is not proof of final inbox arrival. A delivery error or unavailable configuration returns an error and never produces a success confirmation. A network timeout can leave the client unable to confirm submission; its entries stay available for retry or email.

## Local preview

```sh
python3 server/inquiry.py --port 8091
```

Open `http://127.0.0.1:8091/`. Preview validates the form and returns an explicit **not sent** message. It neither sends nor saves inquiries. The development server binds to loopback and is not the production server.

## Checks

```sh
node scripts/prepare-release.mjs --check
node scripts/prepare-release.test.mjs
node scripts/inquiry.test.mjs
python3 -m unittest discover -s server -v
```

The optional production HTTP integration test needs Gunicorn installed in a temporary virtual environment:

```sh
python3 -m venv /tmp/kerrco-inquiry-venv
/tmp/kerrco-inquiry-venv/bin/python -m pip install -r server/requirements.txt
KERRCO_GUNICORN=/tmp/kerrco-inquiry-venv/bin/gunicorn python3 -m unittest discover -s server -v
```

Tests use only loopback SMTP capture and synthetic `.test` addresses. They cover actual Gunicorn HTTP and SMTP acceptance, native HTML and JSON responses, rejected recipients, missing configuration, invalid fields/origins, header injection, body limits, rate limits, and error feedback. The JavaScript checks ensure that only a `201` acknowledgement clears entries; previews, network errors, malformed responses, and server failures preserve them.

The implementation uses Python's [EmailMessage](https://docs.python.org/3/library/email.message.html) and [SMTP client](https://docs.python.org/3/library/smtplib.html), [Gunicorn](https://pypi.org/project/gunicorn/27.0.1/), and Nginx's [proxy header handling](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header).

## Production setup and activation

Publication is a separate step. A static release alone does not install the form backend.

1. Verify the intended source commit, host, existing release, preserved sites, and rollback state. Retain the existing static release and copies of only affected Nginx files/links before changes.
2. Install a source-pinned backend under `/opt/kerrco-inquiry/releases/<source-sha>/server`, with a separate `/opt/kerrco-inquiry/current` link and isolated `/opt/kerrco-inquiry/venv`. Use a dedicated non-login `kerrco-inquiry` account with no SSH, sudo, or access to unrelated application data. Install the pinned requirement without changing the system Python.
3. Configure the approved sender, recipient, SMTP host/port, security mode, and credentials privately. Use `starttls` (normally port 587) or `ssl` (normally port 465) as required by the relay. Do not weaken TLS verification or change unrelated Exim/Certbot settings.
4. Install the service template and verify its configuration/startup. Check that only loopback `8766` is listening. Without a valid delivery configuration, startup must fail.
5. Before enabling the public route, authorize and send one clearly labeled test inquiry to the owner's approved inbox. Confirm actual receipt, correct Reply-To, and a working reply path. SMTP acceptance alone does not satisfy this inbox check. Exercise a failed delivery using an isolated test configuration, then restore the approved configuration; failure must not show success.
6. Add the exact-match route only to the existing `kerrco.us` HTTPS server, using the included Nginx snippet. Preserve all other vhosts and hashes. Run `nginx -t` before every reload. Keep legacy PHP and dotfile rejection intact.
7. Publish the verified static release and test the native and enhanced form paths, failed requests, rate limiting, the email fallback, and all preserved project sites. Do not record request bodies or credentials in deployment evidence.

If activation fails, restore the prior static release and affected Nginx state, test Nginx, and reload only after validation passes. Stop/disable only the new inquiry service if needed. Retain backend releases and sanitized evidence for diagnosis. Keep the public contact address available throughout.
