import json
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")

# Apache combined/common log format: first field is IP, request path is the
# quoted portion between the two quotes, e.g. "GET /index.html HTTP/1.1"
def _compute_ground_truth():
    lines = [l for l in LOG_PATH.read_text().splitlines() if l.strip()]

    ips = []
    paths = []
    for line in lines:
        ip = line.split(" ", 1)[0]
        ips.append(ip)

        start = line.find('"')
        end = line.find('"', start + 1)
        request_line = line[start + 1:end] if start != -1 and end != -1 else ""
        parts = request_line.split()
        if len(parts) >= 2:
            paths.append(parts[1])

    total_requests = len(lines)
    unique_ips = len(set(ips))
    path_counts = Counter(paths)
    top_path, top_path_count = path_counts.most_common(1)[0]

    return {
        "total_requests": total_requests,
        "unique_ips": unique_ips,
        "top_path": top_path,
        "top_path_count": top_path_count,
    }


def test_report_exists():
    """The agent produced a report file."""
    assert REPORT_PATH.exists(), "no report.json found"


def test_report_is_valid_json():
    """The report file contains valid, non-empty JSON."""
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    try:
        json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_report_has_required_fields():
    """The report contains all required keys."""
    data = json.loads(REPORT_PATH.read_text())
    required = {"total_requests", "unique_ips", "top_path", "top_path_count"}
    missing = required - data.keys()
    assert not missing, f"report.json missing fields: {missing}"


def test_report_values_correct():
    """The report's values match ground truth computed from access.log."""
    data = json.loads(REPORT_PATH.read_text())
    expected = _compute_ground_truth()

    assert data["total_requests"] == expected["total_requests"], (
        f"total_requests: expected {expected['total_requests']}, got {data['total_requests']}"
    )
    assert data["unique_ips"] == expected["unique_ips"], (
        f"unique_ips: expected {expected['unique_ips']}, got {data['unique_ips']}"
    )
    assert data["top_path"] == expected["top_path"], (
        f"top_path: expected {expected['top_path']}, got {data['top_path']}"
    )
    assert data["top_path_count"] == expected["top_path_count"], (
        f"top_path_count: expected {expected['top_path_count']}, got {data['top_path_count']}"
    )