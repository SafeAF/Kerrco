# Inquiry backend setup — November 24, 2026

Samuel saved the Gmail app password privately on the existing server after requesting the inquiry form and choosing Gmail delivery. This record covers the backend installation, not publication of the refreshed website or activation of a public form route.

## Installed state

- Source: clean `main`, commit `16ee369d2e3f8d5c3026b30ea7e7d892b0931bea`.
- Host/operator: `proxy-1` (`proxy1`), existing `keystone` deployment identity and noninteractive sudo.
- Backend release: `/opt/kerrco-inquiry/releases/16ee369d2e3f8d5c3026b30ea7e7d892b0931bea`; `/opt/kerrco-inquiry/current` points to it.
- Isolated runtime: `/opt/kerrco-inquiry/venv`, Python 3.11.2 and pinned Gunicorn 27.0.1.
- Account: system user/group `kerrco-inquiry`, non-login shell, no created home directory.
- Unit: `/etc/systemd/system/kerrco-inquiry.service`, enabled and active, listening only on `127.0.0.1:8766`.
- Configuration: `/etc/kerrco-inquiry.env`, root-owned mode `0600`. No credential is included in source, this record, or setup output.
- Setup timestamp: `2026-11-24T17:29:01Z`.
- Protected evidence: `/var/lib/kerrco-deploy/artifacts/inquiry-20261124T172901Z-16ee369d`.
- Backend archive SHA-256: `3640da051fb67ba53dc1716f2fd031dc15b1aa97a5b08ed9be3a24e9e9f3d3f7`.

Google's display spaces had been pasted with the app password. Only that whitespace was removed, using a private atomic replacement that retained root-only permissions. Configuration identity was checked against the approved Gmail address, `smtp.gmail.com:587`, STARTTLS, and the canonical site origin. Gmail authenticated successfully over verified TLS; this authentication check sent no email.

## Verification

- All 17 backend tests passed locally for the committed source, including actual Gunicorn HTTP and loopback SMTP capture. All three inquiry-client tests passed. These tests sent no external email.
- Uploaded archive and extracted file hashes matched the source manifest.
- `systemd-analyze verify` passed before starting the new service.
- Actual service HTTP requests rejected GET with 405, an untrusted origin with 403, and an invalid form with 422. None reached mail delivery.
- `nginx -t` passed. Before/after hashes and symlink targets under `/etc/nginx` matched exactly; Nginx was not reloaded.
- The public static release remains `/var/www/kerrco/releases/20261124T004511Z-d479e05-3ea05818`.
- The new service remained enabled/active and listened only on loopback. The configuration retained root ownership and mode `0600`. Kerrco, Weather, Funds, and Water Ordering all returned HTTPS 200 after installation.

## Authorized delivery test

Samuel explicitly approved sending one test inquiry from and to `kerrcoenterprises@gmail.com`, containing `TEST ONLY — KERRCO inquiry-form delivery check`. Exactly one POST was made to the running backend at `2026-11-24T17:30:57Z`; it returned HTTP 201 with `ok: true` after Gmail SMTP acceptance. The fixed subject is `KERRCO software consultation inquiry`. The test was not retried. Sanitized evidence is in `test-inquiry.json` beside the installation record on the server.

Samuel confirmed actual receipt on November 24, 2026 by answering “Received it” to the delivery-check question. This establishes receipt of the single authorized test in addition to SMTP acceptance. No separate manual reply test is recorded.

## Subsequent public activation

After confirming receipt, Samuel requested deployment. The refreshed website and exact Nginx `/inquiries` route were activated at `2026-11-24T17:39:41Z`; see [the public deployment record](2026-11-24-consulting-refresh.md). The backend release and private Gmail configuration were unchanged, and no additional email was sent during deployment.

The backend still binds only to loopback; Nginx now exposes its exact inquiry route. Stopping the service would make public submissions unavailable. For a full rollback, follow the public deployment record and preserve the backend source release, runtime, evidence, and root-only credential file. The earlier backend-only setup did not change the static site or Nginx.
