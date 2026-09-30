import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_login_successful(page, login_page, credentials):
    """Verify successful login with valid credentials."""
    user = credentials["valid_user"]

    login_page.login(user["username"], user["password"])

    # Built here rather than via the inventory_page fixture, which logs in itself.
    inventory_page = InventoryPage(page)
    expect(page).to_have_url(inventory_page.url_pattern)
    expect(inventory_page.title).to_have_text("Products")


@pytest.mark.parametrize(
    ("user_key", "expected_error"),
    [
        pytest.param(
            "invalid_user",
            "Username and password do not match any user in this service",
            id="invalid-credentials",
            marks=pytest.mark.smoke,
        ),
        pytest.param("locked_out_user", "Sorry, this user has been locked out.", id="locked-out-user"),
        pytest.param("missing_username", "Username is required", id="missing-username"),
        pytest.param("missing_password", "Password is required", id="missing-password"),
    ],
)
def test_login_rejected(login_page, credentials, user_key, expected_error):
    """Verify invalid logins are rejected with the right error.

    The test PASSES when the application refuses the login as expected.
    """
    user = credentials[user_key]

    login_page.login(user["username"], user["password"])

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(expected_error)
    expect(login_page.page).to_have_url(login_page.url_pattern)


def test_logout_returns_to_login(inventory_page, login_page):
    """Verify logging out returns to the login page."""
    inventory_page.header.logout()

    expect(login_page.page).to_have_url(login_page.url_pattern)
    expect(login_page.login_button).to_be_visible()
