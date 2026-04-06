import pytest
import logging

from tests.pages import CheckoutPage, InventoryPage, LoginPage

logger = logging.getLogger(__name__)

class TestOrderPlacement:
    """End-to-end order placement scenarios for SauceDemo."""

    def test_successful_login(self, login_page):
        """Verify a standard user can log in successfully."""
        logger.info("Entering test_successful_login")
        inventory_page = login_page.login("standard_user", "secret_sauce")
        assert inventory_page.page.url == InventoryPage.URL
        assert inventory_page.locator('.title').text_content() == "Products"

    def test_add_item_to_cart(self, logged_in_page):
        """Verify a user can add an item to the cart from the inventory page."""
        logger.info("Entering test_add_item_to_cart")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        assert inventory_page.locator('[data-test="remove-sauce-labs-backpack"]').is_visible()
        assert inventory_page.cart_count() == 1

    def test_view_cart(self, logged_in_page):
        """Verify the cart page displays selected items."""
        logger.info("Entering test_view_cart")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        cart_page = inventory_page.go_to_cart()
        assert cart_page.page.url == cart_page.URL
        assert cart_page.item_count() == 1

    def test_checkout_step_one(self, logged_in_page):
        """Verify the first checkout step accepts valid customer info."""
        logger.info("Entering test_checkout_step_one")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        assert checkout_page.page.url == CheckoutPage.STEP_TWO_URL

    def test_checkout_step_two_and_complete(self, logged_in_page):
        """Verify the checkout can complete and show the confirmation page."""
        logger.info("Entering test_checkout_step_two_and_complete")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        confirmation_page = checkout_page.finish_order()
        assert confirmation_page.page.url == confirmation_page.URL
        assert confirmation_page.confirmation_text() == "Thank you for your order!"

    def test_checkout_with_empty_fields(self, logged_in_page):
        """Verify checkout validation triggers when required fields are empty."""
        logger.info("Entering test_checkout_with_empty_fields")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.continue_checkout()
        assert "First Name is required" in checkout_page.error_text()

    def test_checkout_with_invalid_data(self, logged_in_page):
        """Verify the checkout process accepts invalid but present field input."""
        logger.info("Entering test_checkout_with_invalid_data")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("123", "456", "abc")
        checkout_page.continue_checkout()
        assert checkout_page.page.url == CheckoutPage.STEP_TWO_URL

    def test_remove_item_from_cart(self, logged_in_page):
        """Verify an item can be removed from the cart before checkout."""
        logger.info("Entering test_remove_item_from_cart")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        cart_page = inventory_page.go_to_cart()
        cart_page.remove_product("sauce-labs-backpack")
        assert cart_page.item_count() == 0

    def test_continue_shopping(self, cart_with_items_page):
        """Verify Continue Shopping returns the user to the inventory page."""
        logger.info("Entering test_continue_shopping")
        inventory_page = cart_with_items_page
        cart_page = inventory_page.go_to_cart()
        inventory_page = cart_page.continue_shopping()
        assert inventory_page.page.url == InventoryPage.URL
