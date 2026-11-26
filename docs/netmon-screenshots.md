# NetMon screenshot provenance — November 26, 2026

The owner requested a local NetMon instance populated with fake data and actual application screenshots for the Kerrco site. The homepage's fourth project tab and the NetMon portfolio entry use two browser captures from that instance. Both images include an in-app **SYNTHETIC DEMO DATA** banner, and the website captions repeat that qualification.

## Isolated application

- Source: clean local `/home/sam/source/network_monitor`, commit `7f57a0b0fee5f4bf2ad30a942dc5373a9a2a71b8`. This local branch was five commits behind its recorded `origin/main`; no fetch, checkout update, or upstream change was performed.
- Application copy: `/tmp/kerrco-netmon-demo-20261126-7prvg6tu/netmon`.
- Database: a new `storage/kerrco_demo.sqlite3` inside that disposable copy, created through its existing migrations. No existing NetMon database was opened or copied.
- Runtime: Ruby 3.4.10, Rails 8.0.4, Puma 7.2.0, bound to `127.0.0.1:8116`. The lockfile's dependencies, including Bundler 2.6.2, were installed into a separate bundle under the same `/tmp` directory. Existing JavaScript dependencies were read to build the isolated copy's assets.
- Credentials, environment files, existing storage/log/tmp directories, and deployment secrets were excluded from the copy. The source checkout's 242 copied source-file fingerprints were unchanged after capture.
- No router agent, conntrack ingestion, DNS collection, host enrichment, or traceroute was run. The capture browser blocked requests outside the local application origin.

The isolated copy has a screenshot-only initializer that supplies fictional `/proc` and network-interface metrics, disables live metric recording and mail delivery, and freezes the server clock at the fixture timestamp. The browser's date clock matches it. This keeps relative-time windows stable between captures. A banner was added to the disposable layout; the application views, charts, incident grouping display, and controls otherwise render from the copied source. These fixture changes were not made to the NetMon checkout or deployed as application code.

## Synthetic records

Seed `20261126` creates the following records through the application models in one transaction, guarded against any database path except the disposable target and against a nonempty fixture database:

| Records | Count |
| --- | ---: |
| Fictional devices | 8 |
| Remote hosts using example addresses | 32 |
| Connections | 56 |
| DNS events and answers | 56 each |
| Grouped incidents | 4 |
| Anomaly hits | 15 |
| Device-minute / remote-host-minute records | 480 / 1,920 |
| Metric / system-minute samples | 60 each |

Device names, `.test` domains, example IP addresses, traffic volumes, scores, incident reasons, system load, memory, interfaces, and the sample heartbeat are fictional. The fixture clock is `2026-11-26T16:55:36Z`. The images demonstrate the application's presentation and review controls; they do not establish collector operation, detector accuracy, or a customer result.

## Published assets

| Asset | Dimensions | SHA-256 |
| --- | --- | --- |
| `web/assets/img/rework/netmon-dashboard-screen.jpg` | 1440 × 1000 | `0b1581e28591ba129df98a1b8de0a16a50dcb473e90a6aa4e78ab68b36fe5d82` |
| `web/assets/img/rework/netmon-incidents-screen.jpg` | 1440 × 820 | `983ce62114116d5c26de081b5e3d2a7de75aa55c1b10cfefb5f6cfb40c13572d` |

Captured with the installed headless Chromium at approximately 10:02 a.m. MST on November 26, 2026. The ordinary browser connection reported its access host unavailable. The dashboard's native filter control is collapsed; the incident page's first Recent hits disclosure is expanded. Capture selects the browser viewport and writes JPEG directly. No interface values were painted over or image content edited. Both images were visually inspected; the final dashboard frame ends after the charts rather than clipping the following incident panel.

Reproduction and verification evidence is in ignored `artifacts/netmon-captures-2026-11-26/`: source fingerprints, seed script, fixture counts, demo initializer/layout, disposable database snapshot, capture script, image hashes, and website review results. Publication and rollback details are recorded separately in the deployment log.

## Website checks

Headless Chromium checked the homepage and portfolio at 1440, 768, 375, and 320px. All visible images decoded; there was no horizontal page overflow or page JavaScript error. The four-tab order, initial Weather selection, pointer selection, Left/Right wraparound, Home/End, tab-stop state, and focus entering the active NetMon panel passed at all four widths. All four project panels remained readable without JavaScript. Homepage-to-portfolio navigation and both full-size image links passed. Desktop and phone captures were visually inspected.

Static validation passed for 11 pages, 370 references, 42 image elements, and 56 public release files. All seven release-validator tests and whitespace checks passed. No inquiry was submitted. These checks establish the tested layouts and controls, not full accessibility certification or the accuracy of NetMon's detection rules. The temporary NetMon capture server was stopped after capture.
