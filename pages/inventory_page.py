from playwright.sync_api import Locator, Page

from pages.base_page import AppPage


class InventoryPage(AppPage):
    """Page Object for the product listing page."""

    PATH = "/inventory.html"

    SORT_NAME_ASC = "az"
    SORT_NAME_DESC = "za"
    SORT_PRICE_ASC = "lohi"
    SORT_PRICE_DESC = "hilo"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.sort_select = page.get_by_test_id("product-sort-container")

    def item(self, name: str) -> Locator:
        return self.items.filter(
            has=self.page.get_by_test_id("inventory-item-name").get_by_text(name, exact=True)
        )

    def add_to_cart(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Remove").click()

    def sort_by(self, option: str) -> None:
        self.sort_select.select_option(option)

    def products(self) -> list[tuple[str, float]]:
        """Snapshot of (name, price) for every listed product, in display order."""
        self.items.first.wait_for()
        names = self.item_names.all_inner_texts()
        prices = [self.parse_price(p) for p in self.item_prices.all_inner_texts()]
        return list(zip(names, prices))
