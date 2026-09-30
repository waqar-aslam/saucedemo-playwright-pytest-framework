import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.regression


@pytest.fixture
def checkout_info(inventory_page, cart_page, checkout_info_page, products):
    """Checkout step one, with the test products in the cart."""
    for name in products:
        inventory_page.add_to_cart(name)
    inventory_page.header.open_cart()
    cart_page.checkout()
    return checkout_info_page


@pytest.mark.smoke
def test_complete_checkout(
    checkout_info, checkout_overview_page, checkout_complete_page, customer, products
):
    """Verify a customer can place an order end to end."""
    checkout_info.fill_customer(**customer)
    checkout_info.continue_to_overview()

    expect(checkout_overview_page.page).to_have_url(checkout_overview_page.url_pattern)
    expect(checkout_overview_page.item_names).to_have_text(products)

    checkout_overview_page.finish()

    expect(checkout_complete_page.page).to_have_url(checkout_complete_page.url_pattern)
    expect(checkout_complete_page.complete_header).to_have_text("Thank you for your order!")
    expect(checkout_complete_page.header.cart_badge).to_be_hidden()


def test_order_totals_are_consistent(checkout_info, checkout_overview_page, customer):
    """Verify item total = sum of item prices, and total = item total + tax."""
    checkout_info.fill_customer(**customer)
    checkout_info.continue_to_overview()
    expect(checkout_overview_page.total_label).to_be_visible()

    subtotal = checkout_overview_page.subtotal()

    assert subtotal == checkout_overview_page.item_prices_total()
    assert checkout_overview_page.total() == round(subtotal + checkout_overview_page.tax(), 2)


@pytest.mark.parametrize(
    ("missing_field", "expected_error"),
    [
        pytest.param("first_name", "First Name is required", id="missing-first-name"),
        pytest.param("last_name", "Last Name is required", id="missing-last-name"),
        pytest.param("postal_code", "Postal Code is required", id="missing-postal-code"),
    ],
)
def test_checkout_requires_customer_info(
    checkout_info, customer, missing_field, expected_error
):
    """Verify each customer field is mandatory."""
    checkout_info.fill_customer(**{**customer, missing_field: ""})
    checkout_info.continue_to_overview()

    expect(checkout_info.error_message).to_contain_text(expected_error)
    expect(checkout_info.page).to_have_url(checkout_info.url_pattern)
