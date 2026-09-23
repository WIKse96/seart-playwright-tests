import os

import pytest
from dotenv import load_dotenv

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
    return int(os.environ.get("PAGE_LOAD_THRESHOLD_MS", "8000"))


@pytest.fixture
def accept_cookies(page):
    def _accept():
        reject_button = page.get_by_role("button", name="Odrzuć")
        try:
            reject_button.click(timeout=5000)
        except Exception:
            pass

    return _accept
