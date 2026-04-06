from __future__ import annotations

import logging

from .base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Page object for the SauceDemo cart screen."""

    URL = "https://www.saucedemo.com/cart.html"
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'
    CART_ITEM = ".cart_item"
    PRODUCT_NAME = ".inventory_item_name"

    def item_count(self) -> int:
        """Return the number of items currently in the cart."""
        logger.info("Counting cart items")
        return self.locator(self.CART_ITEM).count()

    def item_names(self) -> list[str]:
        """Return the list of product names currently in the cart."""
        logger.info("Getting cart item names")
        return [item.text_content() or "" for item in self.locator(self.PRODUCT_NAME).all()]

    def checkout(self) -> "CheckoutPage":
        """Proceed to the checkout page from the cart."""
        from .checkout_page import CheckoutPage

        logger.info("Proceeding to checkout")
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url(CheckoutPage.STEP_ONE_URL)
        return CheckoutPage(self.page)

    def continue_shopping(self) -> "InventoryPage":
        """Return to the inventory page from the cart."""
        from .inventory_page import InventoryPage

        logger.info("Continuing shopping")
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_url(InventoryPage.URL)
        return InventoryPage(self.page)

    def remove_product(self, product_id: str) -> None:
        """Remove a product from the cart by its identifier."""
        logger.info("Removing product %s from cart", product_id)
        self.click(f'[data-test="remove-{product_id}"]')

    def has_checkout_button(self) -> bool:
        """Return whether the checkout button is visible on the cart page."""
        logger.info("Checking checkout button visibility")
        return self.locator(self.CHECKOUT_BUTTON).is_visible()
