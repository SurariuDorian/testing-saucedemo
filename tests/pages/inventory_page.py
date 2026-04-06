from __future__ import annotations

import logging

from .base_page import BasePage

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """Page object for the SauceDemo inventory screen."""

    URL = "https://www.saucedemo.com/inventory.html"
    SORT_CONTAINER = ".product_sort_container"
    CART_LINK = ".shopping_cart_link"
    PRODUCT_ITEM = ".inventory_item"
    PRODUCT_NAME = ".inventory_item_name"
    PRODUCT_IMAGE = ".inventory_item_img img"
    PRODUCT_PRICE = ".inventory_item_price"
    CART_BADGE = ".shopping_cart_badge"
    MENU_BUTTON = '#react-burger-menu-btn'
    LOGOUT_LINK = '#logout_sidebar_link'

    def add_to_cart(self, product_id: str) -> None:
        """Add the specified product to the shopping cart."""
        logger.info("Adding product %s to cart", product_id)
        self.click(f'[data-test="add-to-cart-{product_id}"]')

    def remove_from_cart(self, product_id: str) -> None:
        """Remove the specified product from the shopping cart."""
        logger.info("Removing product %s from cart", product_id)
        self.click(f'[data-test="remove-{product_id}"]')

    def add_all_products(self) -> None:
        """Add every available product on the inventory page to the cart."""
        logger.info("Adding all products to cart")
        while self.locator('[data-test^="add-to-cart"]').count() > 0:
            self.locator('[data-test^="add-to-cart"]').first.click()

    def product_count(self) -> int:
        """Return the number of product cards displayed."""
        logger.info("Counting product cards")
        return self.locator(self.PRODUCT_ITEM).count()

    def product_titles(self) -> list[str]:
        """Return a list of product titles currently displayed."""
        logger.info("Getting product titles")
        return [item.text_content() or "" for item in self.locator(self.PRODUCT_NAME).all()]

    def sort_products(self, value: str) -> None:
        """Sort the inventory using the given sort option."""
        logger.info("Sorting products by %s", value)
        self.select_option(self.SORT_CONTAINER, value)

    def cart_count(self) -> int:
        """Return the current cart item count displayed in the badge."""
        logger.info("Getting cart badge count")
        badge = self.locator(self.CART_BADGE)
        return int(badge.text_content() or "0") if badge.is_visible() else 0

    def go_to_cart(self) -> "CartPage":
        """Navigate from inventory to the cart page."""
        from .cart_page import CartPage

        logger.info("Navigating to cart page")
        self.click(self.CART_LINK)
        self.wait_for_url(CartPage.URL)
        return CartPage(self.page)

    def logout(self) -> "LoginPage":
        """Logout and return to the login page."""
        from .login_page import LoginPage

        logger.info("Logging out from inventory page")
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        self.wait_for_url(LoginPage.URL)
        return LoginPage(self.page)

    def open_first_product(self) -> None:
        """Open the first product detail page."""
        logger.info("Opening first product details")
        self.locator(self.PRODUCT_NAME).first.click()
