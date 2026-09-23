from playwright.sync_api import Page, expect


def test_add_product_to_cart(page: Page, site, accept_cookies):
    page.goto(site.product_url)
    accept_cookies()

    add_to_cart_button = page.locator("button.btn-cart").first
    confirmation = page.get_by_text(site.confirmation_text)

    for attempt in range(3):
        add_to_cart_button.click()
        try:
            expect(confirmation).to_be_visible(timeout=3000)
            break
        except AssertionError:
            if attempt == 2:
                raise
