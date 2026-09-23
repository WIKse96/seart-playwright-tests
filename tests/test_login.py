import re

import pytest
from playwright.sync_api import Page, expect


def test_customer_login(page: Page, site, accept_cookies):
    page.goto(site.login_url)
    accept_cookies()

    email_field = page.get_by_role("textbox", name=site.email_field_name)
    password_field = page.get_by_role("textbox", name=site.password_field_name)
    try:
        expect(email_field).to_be_visible(timeout=10000)
    except AssertionError:
        pytest.fail(f"{site.label} - nie znaleziono formularza logowania")

    credentials = site.credentials
    email_field.fill(credentials["email"])
    password_field.fill(credentials["password"])
    page.get_by_role("button", name=site.login_button_name).click()

    try:
        expect(page).to_have_url(re.compile(r"/customer/account"), timeout=10000)
        expect(page).to_have_title(site.account_page_title, timeout=10000)
    except AssertionError:
        pytest.fail(f"{site.label} - logowanie nie powiodlo sie (strona: {page.title()!r})")
