from playwright.sync_api import Page

from pages.base_page import AppPage


class CheckoutInfoPage(AppPage):
    """Checkout step one: customer information."""

    PATH = "/checkout-step-one.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.get_by_test_id("firstName")
        self.last_name_input = page.get_by_test_id("lastName")
        self.postal_code_input = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.error_message = page.get_by_test_id("error")

    def fill_customer(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_overview(self) -> None:
        self.continue_button.click()


class CheckoutOverviewPage(AppPage):
    """Checkout step two: order summary."""

    PATH = "/checkout-step-two.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.subtotal_label = page.get_by_test_id("subtotal-label")
        self.tax_label = page.get_by_test_id("tax-label")
        self.total_label = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")

    def item_prices_total(self) -> float:
        return round(sum(self.parse_price(p) for p in self.item_prices.all_inner_texts()), 2)

    def subtotal(self) -> float:
        return self.parse_price(self.subtotal_label.inner_text())

    def tax(self) -> float:
        return self.parse_price(self.tax_label.inner_text())

    def total(self) -> float:
        return self.parse_price(self.total_label.inner_text())

    def finish(self) -> None:
        self.finish_button.click()


class CheckoutCompletePage(AppPage):
    """Order confirmation."""

    PATH = "/checkout-complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.complete_header = page.get_by_test_id("complete-header")
        self.back_home_button = page.get_by_test_id("back-to-products")
