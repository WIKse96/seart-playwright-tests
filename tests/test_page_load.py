from playwright.sync_api import Page


def test_product_page_load_time(page: Page, site, page_load_threshold_ms: int):
    page.goto(site.product_url, wait_until="load")

    timing = page.evaluate(
        "() => { const [nav] = performance.getEntriesByType('navigation'); "
        "return { loadEventEnd: nav.loadEventEnd, domContentLoaded: nav.domContentLoadedEventEnd }; }"
    )

    load_time_ms = timing["loadEventEnd"]
    dom_content_loaded_ms = timing["domContentLoaded"]

    print(f"\n[{site.id}] Czas ladowania strony (load event): {load_time_ms:.0f} ms")
    print(f"[{site.id}] Czas do DOMContentLoaded: {dom_content_loaded_ms:.0f} ms")

    assert load_time_ms > 0, "Nie udalo sie zmierzyc czasu ladowania strony"
    assert load_time_ms < page_load_threshold_ms, (
        f"[{site.id}] Strona ladowala sie {load_time_ms:.0f} ms, "
        f"co przekracza limit {page_load_threshold_ms} ms"
    )
