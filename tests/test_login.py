import re

from playwright.sync_api import Page, expect


def test_customer_login(page: Page, login_url: str, login_credentials: dict, accept_cookies):
    page.goto(login_url)
    accept_cookies()

    page.get_by_role("textbox", name="Adres e-mail").fill(login_credentials["email"])
    page.get_by_role("textbox", name="Hasło").fill(login_credentials["password"])
    page.get_by_role("button", name="Logowanie").click()

    expect(page).to_have_url(re.compile(r"/customer/account"))
    expect(
        page.get_by_role("link", name=re.compile("Wyloguj", re.IGNORECASE)).first
    ).to_be_visible(timeout=10000)
