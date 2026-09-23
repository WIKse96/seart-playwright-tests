from playwright.sync_api import Page, expect


def test_add_product_to_cart(page: Page, site, accept_cookies):
    page.goto(site.product_url)
    accept_cookies()

    page.locator("button.btn-cart").first.click()

    expect(page.get_by_text(site.confirmation_text)).to_be_visible(timeout=10000)
