# Reproduce workflow verification

The evidence contains real n8n 2.41.3 CLI executions and emails accepted by a local SMTP capture service. JSON files contain node output and execution status; local authentication tokens and execution resume tokens are omitted. `local-mail.ndjson` contains the actual captured email content. A failed notification is intentionally a failed execution. Successful fallback delivery is marked success with an explicit warning/error subject.

| Scenario | Temporary change in n8n | Expected result | Recorded evidence |
| --- | --- | --- | --- |
| Normal digest | None | HIGH ACTIVITY; SMTP acceptance | n8n-success.json |
| Source API fails | Get public posts URL: `https://jsonplaceholder.typicode.com/does-not-exist` | SOURCE ERROR email | n8n-source-error.json |
| Enrichment fails | Get top post comments URL: same invalid endpoint | PARTIAL DATA email; five posts retained | n8n-enrichment-error.json |
| SMTP unavailable | Select a temporary local credential with unreachable host/port | Failed execution, SMTP delivery error | n8n-delivery-error.log |
| App healthy | Ping running local API root | Status 200; healthy log; no email | n8n-uptime-healthy.json |
| App returns 404 | Append `not-found` to app root URL | Uptime alert email with 404 | n8n-uptime-alert.json |

Use Execute workflow after each change and inspect Output and the inbox. Restore URLs/credentials before saving your final exports. An unavailable external email provider is not equivalent to a public-data-source error.

`setup-verification.json` records the fresh setup and launch check. Docker was unavailable here; the Compose configuration is supplied for Windows/Docker use and was not executed here. Required genuine n8n canvas/output screenshots remain a local capture step; JSON evidence is not a screenshot replacement. The schedule and webhook triggers are included but execution evidence uses the manual trigger. Optional daily uptime summaries and persistent incident deduplication are not implemented.
