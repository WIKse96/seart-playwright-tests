import pytest
from playwright.sync_api import Page, expect


def test_add_product_to_cart(page: Page, site, accept_cookies):
    page.goto(site.product_url)
    accept_cookies()

    add_to_cart_button = page.locator("button.btn-cart").first
    try:
        expect(add_to_cart_button).to_be_visible(timeout=10000)
    except AssertionError:
        pytest.fail(f"{site.label} - nie znaleziono przycisku dodaj do koszyka")

    confirmation = page.get_by_text(site.confirmation_text)

    for attempt in range(3):
        add_to_cart_button.click()
        try:
            expect(confirmation).to_be_visible(timeout=3000)
            return
        except AssertionError:
            continue

    pytest.fail(f"{site.label} - nie pojawil sie komunikat potwierdzenia dodania do koszyka")
