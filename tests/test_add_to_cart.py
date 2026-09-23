import re

from playwright.sync_api import Page, expect


def test_add_product_to_cart(page: Page, product_url: str, accept_cookies):
    page.goto(product_url)
    accept_cookies()

    cart_summary = page.locator(".cart-sum")
    expect(cart_summary).to_contain_text("0 produkt")

    page.get_by_role("button", name="Do koszyka").click()

    expect(
        page.get_by_text("Komoda drewniana Rustyk 3/9 został dodany do Twojego koszyka.")
    ).to_be_visible(timeout=10000)
    expect(cart_summary).to_contain_text(re.compile(r"1 produkt"))
