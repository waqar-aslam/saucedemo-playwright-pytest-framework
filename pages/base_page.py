import re

from playwright.sync_api import Page


class BasePage:
    """Common functionality shared by page objects.

    Page objects expose locators and actions only; assertions live in tests.
    PATH is relative to the configured base_url.
    """

    PATH = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.PATH)
        return self

    @property
    def url_pattern(self) -> re.Pattern:
        """Pattern matching this page's URL, for expect(page).to_have_url()."""
        return re.compile(re.escape(self.PATH) + r"$")


class Header:
    """Header and side menu shared by every page after login."""

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()


class AppPage(BasePage):
    """Base for pages shown after login."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.title = page.get_by_test_id("title")

    @staticmethod
    def parse_price(text: str) -> float:
        """Extract the amount from text such as '$29.99' or 'Tax: $2.40'."""
        match = re.search(r"\$(\d+(?:\.\d+)?)", text)
        if match is None:
            raise ValueError(f"No price found in: {text!r}")
        return float(match.group(1))
