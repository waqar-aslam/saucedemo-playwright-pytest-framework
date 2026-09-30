import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import DataLoader


# --- Test data -------------------------------------------------------------

@pytest.fixture(scope="session")
def credentials() -> dict:
    return DataLoader.credentials()


@pytest.fixture(scope="session")
def test_data() -> dict:
    return DataLoader.test_data()


@pytest.fixture(scope="session")
def customer(test_data) -> dict:
    return test_data["customer"]


@pytest.fixture(scope="session")
def products(test_data) -> list[str]:
    return test_data["products"]


# --- Page objects (all share the test's single `page`) ---------------------

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Login page, already opened."""
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(page: Page, login_page: LoginPage, credentials) -> InventoryPage:
    """Inventory page, reached by logging in as the valid user."""
    user = credentials["valid_user"]
    login_page.login(user["username"], user["password"])
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)
