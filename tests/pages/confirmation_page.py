from __future__ import annotations

import logging

from .base_page import BasePage

logger = logging.getLogger(__name__)


class ConfirmationPage(BasePage):
    """Page object for the SauceDemo order confirmation screen."""

    URL = "https://www.saucedemo.com/checkout-complete.html"
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_TO_PRODUCTS_BUTTON = '[data-test="back-to-products"]'
    CART_BADGE = '.shopping_cart_badge'
    BACK_BUTTON = '[data-test="back-to-products"]'

    def confirmation_text(self) -> str:
        """Return the confirmation header text."""
        logger.info("Reading confirmation header text")
        return self.text_content(self.COMPLETE_HEADER)

    def has_pony_express(self) -> bool:
        """Return whether the Pony Express graphic is visible."""
        logger.info("Checking Pony Express visibility")
        return self.locator('.pony_express').is_visible()

    def back_to_products(self) -> "InventoryPage":
        """Return to the inventory page from the confirmation page."""
        from .inventory_page import InventoryPage

        logger.info("Returning to inventory from confirmation page")
        self.click(self.BACK_TO_PRODUCTS_BUTTON)
        self.wait_for_url(InventoryPage.URL)
        return InventoryPage(self.page)

    def cart_badge_visible(self) -> bool:
        """Return whether the cart badge is visible on the confirmation screen."""
        logger.info("Checking cart badge visibility on confirmation page")
        return self.locator(self.CART_BADGE).is_visible()
