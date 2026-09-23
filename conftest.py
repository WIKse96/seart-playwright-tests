import os
import sys

import pytest
from dotenv import load_dotenv

from notifications import send_email_notification, send_ntfy_notification

load_dotenv()


@pytest.fixture(scope="session")
def product_url() -> str:
    return os.environ.get(
        "SEART_PRODUCT_URL",
        "https://www.seart.pl/drewniana-komoda-sosnowa-rustyk-3-9.html",
    )


@pytest.fixture(scope="session")
def login_url() -> str:
    return "https://www.seart.pl/customer/account/login/"


@pytest.fixture(scope="session")
def login_credentials() -> dict:
    return {
        "email": os.environ["SEART_LOGIN_EMAIL"],
        "password": os.environ["SEART_LOGIN_PASSWORD"],
    }


@pytest.fixture(scope="session")
def page_load_threshold_ms() -> int:
    return int(os.environ.get("PAGE_LOAD_THRESHOLD_MS", "11000"))


@pytest.fixture
def accept_cookies(page):
    def _accept():
        reject_button = page.get_by_role("button", name="Odrzuć")
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
        subject = f"[seart.pl testy] {len(failed) + len(errors)} problem(y) z {total}"
    else:
        subject = f"[seart.pl testy] wszystko OK ({passed}/{total})"

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
