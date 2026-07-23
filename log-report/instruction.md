There is an Apache-style access log at `/app/access.log`.

Analyze the traffic and write a JSON summary report to `/app/report.json`
with the following fields:

1. `total_requests` — the total number of log lines (requests) in the file.
2. `unique_ips` — the number of distinct client IP addresses.
3. `top_path` — the single most frequently requested path (e.g. `/index.html`).
4. `top_path_count` — how many times `top_path` was requested.

Example output:

```json
{
  "total_requests": 42,
  "unique_ips": 7,
  "top_path": "/index.html",
  "top_path_count": 12
}
```

Save this file exactly at `/app/report.json`.