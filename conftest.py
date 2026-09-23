import os
import sys

import pytest
from dotenv import load_dotenv

from notifications import send_email_notification, send_ntfy_notification
from sites import SITES

load_dotenv()


@pytest.fixture(params=SITES, ids=[s.id for s in SITES])
def site(request):
    return request.param


@pytest.fixture(scope="session")
def page_load_threshold_ms() -> int:
    return int(os.environ.get("PAGE_LOAD_THRESHOLD_MS", "11000"))


@pytest.fixture(autouse=True)
def fail_on_http_error(page):
    errors = []

    def _check(response):
        if response.status >= 400 and response.request.resource_type == "document":
            errors.append(f"{response.status} {response.url}")

    page.on("response", _check)
    yield
    assert not errors, "Strona zwrocila blad HTTP: " + "; ".join(errors)


@pytest.fixture
def accept_cookies(page, site):
    def _accept():
        reject_button = page.get_by_role("button", name=site.cookie_reject_label)
        try:
            reject_button.click(timeout=5000)
        except Exception:
            pass

    return _accept


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    email_enabled = os.environ.get("NOTIFY_EMAIL_ENABLED", "").lower() == "true"
    ntfy_enabled = os.environ.get("NOTIFY_NTFY_ENABLED", "").lower() == "true"
    if not email_enabled and not ntfy_enabled:
        return

    passed = len(terminalreporter.stats.get("passed", []))
    failed = terminalreporter.stats.get("failed", [])
    errors = terminalreporter.stats.get("error", [])
    total = passed + len(failed) + len(errors)

    if failed or errors:
        subject = f"[testy sklepow] {len(failed) + len(errors)} problem(y) z {total}"
    else:
        subject = f"[testy sklepow] wszystko OK ({passed}/{total})"

    lines = [f"Wynik: {passed} passed, {len(failed)} failed, {len(errors)} error (z {total})", ""]
    for report in [*failed, *errors]:
        lines.append(f"- {report.nodeid}")
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
