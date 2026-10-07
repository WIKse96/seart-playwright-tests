import csv
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from dotenv import load_dotenv

from notifications import send_email_notification, send_ntfy_notification
from sites import SITES

load_dotenv()

RESULTS_HISTORY_PATH = Path(__file__).parent / "results_history.csv"


@pytest.fixture(params=SITES, ids=[s.id for s in SITES])
def site(request):
    return request.param


@pytest.fixture(autouse=True)
def fail_on_http_error(page, site):
    errors = []

    def _check(response):
        if response.status >= 400 and response.request.resource_type == "document":
            errors.append(str(response.status))

    page.on("response", _check)
    yield
    if errors:
        pytest.fail(f"{site.label} - strona zwrocila blad HTTP {', '.join(errors)}")


@pytest.fixture
def accept_cookies(page, site):
    def _accept():
        reject_button = page.get_by_role("button", name=site.cookie_reject_label)
        try:
            reject_button.click(timeout=5000)
        except Exception:
            pass

    return _accept


def _failure_reason(report) -> str:
    reprcrash = getattr(report.longrepr, "reprcrash", None)
    message = reprcrash.message if reprcrash is not None else str(report.longrepr)
    message = message.split("\nAria snapshot:")[0].strip()
    max_len = 400
    if len(message) > max_len:
        message = message[:max_len].rstrip() + "..."
    return message


def _site_id_from_nodeid(nodeid: str) -> str | None:
    match = re.search(r"\[([a-zA-Z0-9_]+)-chromium\]", nodeid)
    return match.group(1) if match else None


def _record_results_history(failed, errors) -> None:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return

    site_failures = {s.id: 0 for s in SITES}
    for report in [*failed, *errors]:
        site_id = _site_id_from_nodeid(report.nodeid)
        if site_id in site_failures:
            site_failures[site_id] += 1

    is_new = not RESULTS_HISTORY_PATH.exists()
    with RESULTS_HISTORY_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp_utc", *(s.id for s in SITES)])
        writer.writerow([
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            *(site_failures[s.id] for s in SITES),
        ])


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = len(terminalreporter.stats.get("passed", []))
    failed = terminalreporter.stats.get("failed", [])
    errors = terminalreporter.stats.get("error", [])
    total = passed + len(failed) + len(errors)

    _record_results_history(failed, errors)

    email_enabled = os.environ.get("NOTIFY_EMAIL_ENABLED", "").lower() == "true"
    ntfy_enabled = os.environ.get("NOTIFY_NTFY_ENABLED", "").lower() == "true"
    if not email_enabled and not ntfy_enabled:
        return

    if failed or errors:
        subject = f"[testy sklepow] {len(failed) + len(errors)} problem(y) z {total}"
    else:
        subject = f"[testy sklepow] wszystko OK ({passed}/{total})"

    lines = [f"Wynik: {passed} passed, {len(failed)} failed, {len(errors)} error (z {total})", ""]
    for report in [*failed, *errors]:
        lines.append(f"- {_failure_reason(report)}")
    body = "\n".join(lines)

    if email_enabled:
        try:
            send_email_notification(subject, body)
        except Exception as exc:
            print(f"Nie udalo sie wyslac powiadomienia email: {exc}", file=sys.stderr)

    if ntfy_enabled:
        try:
            send_ntfy_notification(subject, body)
        except Exception as exc:
            print(f"Nie udalo sie wyslac powiadomienia ntfy: {exc}", file=sys.stderr)
