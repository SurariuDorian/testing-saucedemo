import pytest
import logging

logger = logging.getLogger(__name__)

class TestConfirmation:
    """Confirmation and post-order validation tests for SauceDemo."""

    def test_order_complete_page(self, cart_with_items_page):
        """Verify the order confirmation page displays expected completion details."""
        logger.info("Entering test_order_complete_page")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        confirmation_page = checkout_page.finish_order()

        assert confirmation_page.confirmation_text() == "Thank you for your order!"
        assert confirmation_page.locator(confirmation_page.COMPLETE_TEXT).is_visible()
        assert confirmation_page.has_pony_express()

    def test_back_to_products(self, cart_with_items_page):
        """Verify the Back Home button returns the user to the inventory page."""
        logger.info("Entering test_back_to_products")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        confirmation_page = checkout_page.finish_order()
        inventory_page = confirmation_page.back_to_products()

        assert inventory_page.page.url == inventory_page.URL
        assert inventory_page.cart_count() == 0

    def test_complete_order_clears_cart_after_returning_home(self, cart_with_items_page):
        """Verify cart contents are cleared after completing an order and returning home."""
        logger.info("Entering test_complete_order_clears_cart_after_returning_home")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        confirmation_page = checkout_page.finish_order()
        inventory_page = confirmation_page.back_to_products()

        assert inventory_page.cart_count() == 0
        assert inventory_page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').is_visible()
