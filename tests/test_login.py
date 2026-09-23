import re

from playwright.sync_api import Page, expect


def test_customer_login(page: Page, site, accept_cookies):
    page.goto(site.login_url)
    accept_cookies()

    credentials = site.credentials
    page.get_by_role("textbox", name=site.email_field_name).fill(credentials["email"])
    page.get_by_role("textbox", name=site.password_field_name).fill(credentials["password"])
    page.get_by_role("button", name=site.login_button_name).click()

    expect(page).to_have_url(re.compile(r"/customer/account"))
    expect(page).to_have_title(site.account_page_title + " SIMULATED-FAILURE", timeout=10000)
