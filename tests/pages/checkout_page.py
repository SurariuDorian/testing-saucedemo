from __future__ import annotations

import logging

from .base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Page object for SauceDemo checkout screens."""

    BASE_URL = "https://www.saucedemo.com"
    STEP_ONE_URL = f"{BASE_URL}/checkout-step-one.html"
    STEP_TWO_URL = f"{BASE_URL}/checkout-step-two.html"
    FIRST_NAME = '[data-test="firstName"]'
    LAST_NAME = '[data-test="lastName"]'
    POSTAL_CODE = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'
    CANCEL_BUTTON = '[data-test="cancel"]'
    FINISH_BUTTON = '[data-test="finish"]'
    ERROR_MESSAGE = '[data-test="error"]'
    ORDER_SUMMARY = '.summary_info'
    SUBTOTAL_LABEL = '.summary_subtotal_label'
    TAX_LABEL = '.summary_tax_label'
    TOTAL_LABEL = '.summary_total_label'

    def enter_customer_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill in customer information on the checkout form."""
        logger.info("Entering checkout customer info for %s %s", first_name, last_name)
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.POSTAL_CODE, postal_code)

    def continue_checkout(self) -> None:
        """Continue from checkout step one to step two."""
        logger.info("Continuing checkout")
        self.click(self.CONTINUE_BUTTON)

    def cancel(self) -> "InventoryPage":
        """Cancel checkout and return to inventory."""
        from .inventory_page import InventoryPage

        logger.info("Cancelling checkout")
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url(InventoryPage.URL)
        return InventoryPage(self.page)

    def finish_order(self) -> "ConfirmationPage":
        """Finish the order and return the confirmation page."""
        from .confirmation_page import ConfirmationPage

        logger.info("Finishing checkout order")
        self.click(self.FINISH_BUTTON)
        self.wait_for_url(ConfirmationPage.URL)
        return ConfirmationPage(self.page)

    def error_text(self) -> str:
        """Return the checkout error message text."""
        logger.info("Fetching checkout error message")
        return self.text_content(self.ERROR_MESSAGE)

    def has_order_summary(self) -> bool:
        """Return whether the order summary is visible on checkout step two."""
        logger.info("Checking order summary visibility")
        return self.locator(self.ORDER_SUMMARY).is_visible()

    def subtotal(self) -> float:
        """Return the subtotal amount displayed on the checkout page."""
        logger.info("Reading checkout subtotal")
        return float(self.text_content(self.SUBTOTAL_LABEL).split('$')[1])

    def tax(self) -> float:
        """Return the tax amount displayed on the checkout page."""
        logger.info("Reading checkout tax")
        return float(self.text_content(self.TAX_LABEL).split('$')[1])

    def total(self) -> float:
        """Return the total amount displayed on the checkout page."""
        logger.info("Reading checkout total")
        return float(self.text_content(self.TOTAL_LABEL).split('$')[1])
