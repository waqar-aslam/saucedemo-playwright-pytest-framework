import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_inventory_lists_products(inventory_page):
    """Verify the inventory shows the full product catalogue."""
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.items).to_have_count(6)


@pytest.mark.parametrize(
    ("option", "by_price", "reverse"),
    [
        pytest.param(InventoryPage.SORT_NAME_ASC, False, False, id="name-a-to-z"),
        pytest.param(InventoryPage.SORT_NAME_DESC, False, True, id="name-z-to-a"),
        pytest.param(InventoryPage.SORT_PRICE_ASC, True, False, id="price-low-to-high"),
        pytest.param(InventoryPage.SORT_PRICE_DESC, True, True, id="price-high-to-low"),
    ],
)
def test_sort_products(inventory_page, option, by_price, reverse):
    """Verify each sort option orders the products correctly.

    Price sorts compare prices only: products with equal prices may appear in
    either order, so comparing names there would be flaky.
    """
    names, prices = zip(*inventory_page.products())

    inventory_page.sort_by(option)

    if by_price:
        expected = [f"${price:.2f}" for price in sorted(prices, reverse=reverse)]
        expect(inventory_page.item_prices).to_have_text(expected)
    else:
        expect(inventory_page.item_names).to_have_text(sorted(names, reverse=reverse))


def test_cart_badge_tracks_added_and_removed_products(inventory_page, products):
    """Verify the cart badge counts products as they are added and removed."""
    badge = inventory_page.header.cart_badge
    expect(badge).to_be_hidden()

    for count, name in enumerate(products, start=1):
        inventory_page.add_to_cart(name)
        expect(badge).to_have_text(str(count))

    for name in products:
        inventory_page.remove_from_cart(name)

    expect(badge).to_be_hidden()
