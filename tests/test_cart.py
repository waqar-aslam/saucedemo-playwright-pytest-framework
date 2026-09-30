import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_added_products_appear_in_cart(inventory_page, cart_page, products):
    """Verify products added from the inventory are listed in the cart."""
    for name in products:
        inventory_page.add_to_cart(name)

    inventory_page.header.open_cart()

    expect(cart_page.page).to_have_url(cart_page.url_pattern)
    expect(cart_page.item_names).to_have_text(products)


def test_remove_product_from_cart(inventory_page, cart_page, products):
    """Verify removing a product in the cart updates the list and badge."""
    for name in products:
        inventory_page.add_to_cart(name)
    inventory_page.header.open_cart()

    cart_page.remove(products[0])

    expect(cart_page.item_names).to_have_text(products[1:])
    expect(cart_page.header.cart_badge).to_have_text(str(len(products) - 1))


def test_continue_shopping_returns_to_inventory(inventory_page, cart_page):
    """Verify 'Continue Shopping' leads back to the inventory."""
    inventory_page.header.open_cart()

    cart_page.continue_shopping_button.click()

    expect(inventory_page.page).to_have_url(inventory_page.url_pattern)
