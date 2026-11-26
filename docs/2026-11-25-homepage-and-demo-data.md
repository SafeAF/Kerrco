# Homepage evidence and demonstration data — November 25, 2026

## Website revision — deployed

Preserved the existing cream, charcoal, and gold design while replacing the homepage's text-only project cards with existing real weather and financial application captures. The owner selected Weather Analysis as the initial view. Financial Analytics is the second project tab; the irrigation case study remains a separate, always-available link. Both previews remain readable without JavaScript. The project selector now uses two keyboard-accessible tabs, without Previous/Next buttons or a counter.

The opening copy names spreadsheets, repetitive paperwork, and disconnected systems. The primary header invitation now matches the homepage: “Tell me what’s taking your time,” supported by “Free initial conversation. No obligation.” The flat-fee qualification remains “Most projects,” with scope and price agreed before work begins. The introduction connects Samuel's software background with current farming and past framing-contractor experience.

The owner clarified that `order.kerrco.us` contains test data only. The strategy, case-study notes, and public project access notes now reflect that clarification. Irrigation screenshots were subsequently captured with owner-authorized headless Chromium and published in the [irrigation screenshot update](deployments/2026-11-25-irrigation-screenshots.md).

Validation passed for 11 pages, 344 references, 34 image elements, and 52 public release files. All seven release-validator tests passed. JavaScript syntax, shared header invitations, ARIA targets, whitespace, and a Node VM check of tab selection, Left/Right wraparound, Home/End, selection/focus state, inactive-panel isolation, and source fallback passed. These checks do not establish browser rendering or screen-reader behavior.

Local review archive: `artifacts/website-review-2026-11-25T16-48-09-583Z-733629f0.tar.gz`.

Archive SHA-256: `c3121ac4b5db6f99fb74cf11329ecdc1e3c672e87984e710c22fa4f2aba0b19b`.

The shell `tar` subprocess was blocked by the sandbox; Python `tarfile` packaged the staged release instead. All 52 staged files and archived file hashes matched the source manifest. The owner subsequently requested publication. This archive was deployed on November 25 at 9:59 a.m. MST; see the [deployment record](deployments/2026-11-25-homepage-evidence.md).

## Demonstration data — applied to order.kerrco.us

The owner requested additional test data and explicitly authorized scoped `keystone` SSH access with noninteractive `sudo` as the `admin` service account after automatic review rejected that access under the infrastructure checkout's audit-only rules.

Verified target: `app1` / `app-1`, active `salmon.service`, application root `/home/admin/salmon-scheduler/web`, Rails production environment, SQLite database `/home/admin/salmon-scheduler/web/db/production.sqlite3`.

Deployed Git HEAD: `6ccee0ddd10e777c60b8c269ce10a7d2a66e2b49`. All ten model-source fingerprints matched the inspected local source. Existing deployed changes to `app/javascript/application.js` and untracked `config/secrets.yml` were preserved. The local Salmon checkout was also left untouched.

The existing `db/seeds.rb` deletes data and was not used. Batch `kerrco-demo-20261125` added records through the deployed application models and validations in one transaction:

| Records | Added | Total after |
| --- | ---: | ---: |
| Canals | 2 | 5 |
| Headgates | 6 | 15 |
| Fictional shareholders | 4 | 11 users |
| User/headgate assignments | 8 | 14 |
| Orders | 36 | 87 |
| Canal flow readings | 60 | 75 |
| Headgate flow readings | 180 | 225 |
| Labeled demo announcements | 3 | 4 |
| Messages | 0 | 0 |

As of the application date, November 25, the new orders comprise 12 completed, eight currently in effect, four future approved, eight pending, and four rejected. The dates and statuses are illustrative; no physical deliveries are represented. New addresses use `.invalid`; random shareholder passwords were neither printed nor retained. No administrator accounts were added. External email delivery was disabled within the runner.

A full rehearsal validated the batch and rolled back. Apply verified a SQLite backup before writing, checked dates, headgate assignments, statuses, and new-user allotment deductions, and required identical fingerprints for every pre-existing record before committing. Post-commit aggregate counts matched the plan. There were no migrations, seed resets, source deployments, service restarts, or changes to existing records.

An independent post-commit query confirmed the five order-status counts above, no invalid dates in the new batch, and no negative allotments among the new shareholders. Public HTTPS returned 200 and displayed all three labeled demo notices. This verified persisted records and public notices. A subsequent authenticated read-only capture and [screenshot deployment](deployments/2026-11-25-irrigation-screenshots.md) added the current-order and canal views; physical delivery and approval transitions remain untested.

Protected backup: `/home/admin/salmon-scheduler/web/db/kerrco-demo-backups/kerrco-demo-20261125-20261125T165108Z-47817bad.sqlite3`. The backup directory is mode 0700 and the backup file mode 0600; its SQLite integrity check passed before apply.

Backup SHA-256: `6aed59e92d522d79158b473d3e83dfcd08cdc1431b29b7e809446bd58704ee4a`.

Local execution evidence and the exact script/record IDs are under ignored `artifacts/order-demo-2026-11-25/`. Repeating the same batch stops before backup or writes if its records already exist. Any future removal should target the recorded batch IDs through the application model relationships; a full database restore would also revert subsequent work and is not an automatic rollback action.
