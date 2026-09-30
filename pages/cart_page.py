from playwright.sync_api import Page

from pages.base_page import AppPage


class CartPage(AppPage):
    """Page Object for the shopping cart."""

    PATH = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    def remove(self, name: str) -> None:
        self.items.filter(
            has=self.page.get_by_test_id("inventory-item-name").get_by_text(name, exact=True)
        ).get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        self.checkout_button.click()
