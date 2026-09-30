# Automation & QA Assessment - Mukul Choudhary

## Task 1: QA
Tested the Node/Express RealWorld API at upstream commit `30b68e1e881462b2f4164ea09ab4c4f5699c7b0b`. SQLite replaces PostgreSQL only for local testing; application logic is unchanged. Signup, login, create, body edit, delete, deleted-content lookup and requests without a session token were exercised. Seven findings, reproduction steps, severity and a root-cause analysis are in `docs/Task1_QA_Report_MukulChoudhary.pdf`; redacted request/response evidence is in `evidence/qa-results.json`. This is API-level QA, not a claim of complete upstream frontend/browser coverage. A small QA client is included for a local walkthrough.

## Task 2: Morning brief
JSONPlaceholder `/posts` provides free, deterministic sample data without an API key. The Code node validates, sorts by descending ID and keeps five posts. `/posts/{id}/comments` enriches the highest-ID post. Five or more comments selects HIGH ACTIVITY; otherwise the digest uses STANDARD or PARTIAL DATA. IDs are an explicit demo ordering, not a popularity metric. Manual, hourly and webhook triggers are included.

HTTP requests have timeouts and network-error retries. HTTP failures, invalid payloads or empty data produce a SOURCE ERROR email. Enrichment failure produces a posts-only digest. SMTP failure becomes a visible failed execution after limited retries. SMTP connection details stay in n8n Credentials. Both workflows were imported, executed and exported through n8n 2.41.3's CLI; instance ownership metadata was removed from exports for portability.

## Bonus and verification
The uptime workflow checks the tested API every five minutes; any non-200 response or network error sends an alert. Elapsed time includes retries. Healthy checks remain visible in execution history. Live public-API success, source failure, enrichment fallback, deliberate SMTP failure, healthy uptime and non-200 alerts were tested. See `evidence/verification-summary.json` and captured local email. Notifications were accepted by a local SMTP test inbox; external mailbox delivery was not tested.

## Finish submission
Capture the two required n8n screenshots and bonus canvas, record your own explanation video, and push this folder to a public GitHub repository. These screenshots/video and the public repository URL must still be added before submission. No screenshots or video are fabricated.

## Local reproduction

With Node.js 24, Python 3, Git and Docker installed, run from the repository root:

```bash
docker compose up -d
python scripts/setup_demo.py
python scripts/run_demo.py
```

Open n8n at `http://localhost:5678` and import the workflow JSON. Create an SMTP credential with host `mailpit`, port `1025`, SSL/TLS off and STARTTLS disabled for this local test inbox. Select it in each Send email node. The inbox is at `http://localhost:8025`. Workflow Settings use the local test email addresses; keep external SMTP credentials in n8n only.
