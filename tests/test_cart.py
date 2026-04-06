import pytest
import logging

logger = logging.getLogger(__name__)

class TestCart:
    """Shopping cart test scenarios for SauceDemo."""

    def test_add_single_item_to_cart(self, logged_in_page):
        """Verify that a product can be added to the cart."""
        logger.info("Entering test_add_single_item_to_cart")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        assert inventory_page.locator('[data-test="remove-sauce-labs-backpack"]').is_visible()
        assert inventory_page.cart_count() == 1

    def test_add_multiple_items_to_cart(self, logged_in_page):
        """Verify that multiple different products can be added to the cart."""
        logger.info("Entering test_add_multiple_items_to_cart")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        inventory_page.add_to_cart("sauce-labs-bike-light")
        inventory_page.add_to_cart("sauce-labs-bolt-t-shirt")
        assert inventory_page.cart_count() == 3

    def test_add_all_products_to_cart(self, logged_in_page):
        """Verify all inventory products can be added to the cart."""
        logger.info("Entering test_add_all_products_to_cart")
        inventory_page = logged_in_page
        inventory_page.add_all_products()
        assert inventory_page.cart_count() == 6
        cart_page = inventory_page.go_to_cart()
        assert cart_page.item_count() == 6

    def test_cart_persistence_after_refresh(self, logged_in_page):
        """Verify that cart contents persist after a page refresh."""
        logger.info("Entering test_cart_persistence_after_refresh")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        inventory_page.page.reload()
        assert inventory_page.cart_count() == 1
        assert inventory_page.locator('[data-test="remove-sauce-labs-backpack"]').is_visible()

    def test_remove_item_from_inventory(self, logged_in_page):
        """Verify that an item can be removed from the cart from inventory view."""
        logger.info("Entering test_remove_item_from_inventory")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        assert inventory_page.cart_count() == 1
        inventory_page.remove_from_cart("sauce-labs-backpack")
        assert inventory_page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').is_visible()
        assert inventory_page.cart_count() == 0

    def test_view_cart(self, cart_with_items_page):
        """Verify cart page shows the correct items and quantity."""
        logger.info("Entering test_view_cart")
        inventory_page = cart_with_items_page
        cart_page = inventory_page.go_to_cart()
        assert cart_page.item_count() == 2
        assert cart_page.item_names()[0] == "Sauce Labs Backpack"
        assert cart_page.item_names()[1] == "Sauce Labs Bike Light"

    def test_remove_item_from_cart(self, cart_with_items_page):
        """Verify an item can be removed from cart on the cart page."""
        logger.info("Entering test_remove_item_from_cart")
        inventory_page = cart_with_items_page
        cart_page = inventory_page.go_to_cart()
        initial_count = cart_page.item_count()
        cart_page.remove_product("sauce-labs-backpack")
        assert cart_page.item_count() == initial_count - 1

    def test_continue_shopping(self, cart_with_items_page):
        """Verify the Continue Shopping button navigates back to inventory."""
        logger.info("Entering test_continue_shopping")
        inventory_page = cart_with_items_page
        cart_page = inventory_page.go_to_cart()
        inventory_page = cart_page.continue_shopping()
        assert inventory_page.page.url == "https://www.saucedemo.com/inventory.html"

    def test_empty_cart(self, logged_in_page):
        """Verify the cart becomes empty after removing all items."""
        logger.info("Entering test_empty_cart")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        inventory_page.remove_from_cart("sauce-labs-backpack")
        cart_page = inventory_page.go_to_cart()
        assert not cart_page.has_checkout_button() or cart_page.item_count() == 0
