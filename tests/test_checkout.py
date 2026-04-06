import pytest
import logging

logger = logging.getLogger(__name__)

class TestCheckout:
    """Checkout process tests for SauceDemo order placement."""

    def test_initiate_checkout(self, cart_with_items_page):
        """Verify a user can begin checkout from the cart page."""
        logger.info("Entering test_initiate_checkout")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        assert checkout_page.page.url == checkout_page.STEP_ONE_URL

    def test_valid_checkout_information(self, cart_with_items_page):
        """Verify checkout proceeds when required checkout fields are completed."""
        logger.info("Entering test_valid_checkout_information")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        assert checkout_page.page.url == checkout_page.STEP_TWO_URL

    @pytest.mark.parametrize("empty_field,expected_error", [
        ("firstName", "First Name is required"),
        ("lastName", "Last Name is required"),
        ("postalCode", "Postal Code is required"),
    ])
    def test_checkout_empty_fields(self, cart_with_items_page, empty_field, expected_error):
        """Verify the checkout form shows field-specific errors for missing input."""
        logger.info("Entering test_checkout_empty_fields")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.fill(f'[data-test="{empty_field}"]', "")
        checkout_page.continue_checkout()
        assert expected_error in checkout_page.error_text()

    def test_checkout_all_fields_empty(self, cart_with_items_page):
        """Verify that the checkout form reports an error when all fields are empty."""
        logger.info("Entering test_checkout_all_fields_empty")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.continue_checkout()
        assert "First Name is required" in checkout_page.error_text()

    def test_checkout_invalid_characters(self, cart_with_items_page):
        """Verify checkout accepts special characters in user input if validation is not strict."""
        logger.info("Entering test_checkout_invalid_characters")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("123!@#", "456$%^", "abc!@#")
        checkout_page.continue_checkout()
        assert checkout_page.page.url == checkout_page.STEP_TWO_URL

    def test_checkout_long_input(self, cart_with_items_page):
        """Verify the checkout form handles long input values without breaking."""
        logger.info("Entering test_checkout_long_input")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        long_text = "A" * 1000
        checkout_page.enter_customer_info(long_text, long_text, long_text)
        checkout_page.continue_checkout()
        assert checkout_page.page.url == checkout_page.STEP_TWO_URL

    def test_order_summary_review(self, cart_with_items_page):
        """Verify the checkout overview page shows order summary and totals."""
        logger.info("Entering test_order_summary_review")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        assert checkout_page.page.locator('.cart_item').count() == 2
        assert checkout_page.has_order_summary()
        assert checkout_page.locator('.summary_tax_label').is_visible()
        assert checkout_page.locator('.summary_total_label').is_visible()

    def test_checkout_price_totals_are_calculated_correctly(self, cart_with_items_page):
        """Verify that displayed checkout totals match subtotal plus tax."""
        logger.info("Entering test_checkout_price_totals_are_calculated_correctly")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        assert abs(checkout_page.subtotal() + checkout_page.tax() - checkout_page.total()) < 0.01

    def test_checkout_with_all_products_in_cart(self, logged_in_page):
        """Verify checkout can complete when all products are in the cart."""
        logger.info("Entering test_checkout_with_all_products_in_cart")
        inventory_page = logged_in_page
        inventory_page.add_all_products()
        cart_page = inventory_page.go_to_cart()
        assert cart_page.item_count() == 6
        checkout_page = cart_page.checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        assert checkout_page.page.locator('.cart_item').count() == 6
        assert checkout_page.has_order_summary()

    def test_cancel_checkout(self, cart_with_items_page):
        """Verify that Cancel returns the user to the inventory page."""
        logger.info("Entering test_cancel_checkout")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        inventory_page = checkout_page.cancel()
        assert inventory_page.page.url == "https://www.saucedemo.com/inventory.html"

    def test_complete_order(self, cart_with_items_page):
        """Verify the checkout flow completes and lands on the confirmation page."""
        logger.info("Entering test_complete_order")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        confirmation_page = checkout_page.finish_order()
        assert confirmation_page.page.url == confirmation_page.URL
        assert confirmation_page.confirmation_text() == "Thank you for your order!"

    def test_checkout_empty_cart(self, logged_in_page):
        """Verify direct checkout access without a cart is handled gracefully."""
        logger.info("Entering test_checkout_empty_cart")
        inventory_page = logged_in_page
        inventory_page.page.goto("https://www.saucedemo.com/checkout-step-one.html")
        # SauceDemo allows direct navigation to checkout page even with empty cart
        assert inventory_page.page.url == "https://www.saucedemo.com/checkout-step-one.html"
