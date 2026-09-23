import pytest
from playwright.sync_api import Page


def test_product_page_load_time(page: Page, site):
    page.goto(site.product_url, wait_until="load")

    timing = page.evaluate(
        "() => { const [nav] = performance.getEntriesByType('navigation'); "
        "return { loadEventEnd: nav.loadEventEnd, domContentLoaded: nav.domContentLoadedEventEnd }; }"
    )

    load_time_ms = timing["loadEventEnd"]
    dom_content_loaded_ms = timing["domContentLoaded"]

    print(f"\n[{site.label}] Czas ladowania strony (load event): {load_time_ms:.0f} ms")
    print(f"[{site.label}] Czas do DOMContentLoaded: {dom_content_loaded_ms:.0f} ms")

    if load_time_ms <= 0:
        pytest.fail(f"{site.label} - nie udalo sie zmierzyc czasu ladowania strony")
    if load_time_ms >= site.load_threshold_ms:
        pytest.fail(
            f"{site.label} - czas ladowania {load_time_ms:.0f} ms zamiast limitu {site.load_threshold_ms} ms"
        )
