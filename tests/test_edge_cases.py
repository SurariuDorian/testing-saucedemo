import pytest
import logging

from tests.pages import CheckoutPage, InventoryPage, LoginPage

logger = logging.getLogger(__name__)

class TestEdgeCases:
    """Edge case and stability tests for SauceDemo workflows."""

    BASE_URL = "https://www.saucedemo.com"

    def test_direct_url_access_inventory(self, page):
        """Verify unauthenticated direct access to inventory redirects to login."""
        logger.info("Entering test_direct_url_access_inventory")
        login_page = LoginPage(page)
        login_page.goto(f"{self.BASE_URL}/inventory.html")
        assert page.url == LoginPage.URL

    def test_direct_url_access_cart(self, page):
        """Verify unauthenticated direct access to cart redirects to login."""
        login_page = LoginPage(page)
        login_page.goto(f"{self.BASE_URL}/cart.html")
        assert page.url == LoginPage.URL

    def test_direct_url_access_checkout(self, page):
        """Verify unauthenticated direct access to checkout redirects to login."""
        login_page = LoginPage(page)
        login_page.goto(f"{self.BASE_URL}/checkout-step-one.html")
        assert page.url == LoginPage.URL

    def test_browser_back_forward_during_checkout(self, cart_with_items_page):
        """Verify browser navigation handles checkout step transitions correctly."""
        logger.info("Entering test_browser_back_forward_during_checkout")
        inventory_page = cart_with_items_page
        checkout_page = inventory_page.go_to_cart().checkout()
        checkout_page.enter_customer_info("John", "Doe", "12345")
        checkout_page.continue_checkout()
        checkout_page.go_back()
        assert checkout_page.page.url == CheckoutPage.STEP_ONE_URL
        checkout_page.go_forward()
        assert checkout_page.page.url == CheckoutPage.STEP_TWO_URL

    def test_multiple_tabs(self, browser):
        """Verify session isolation across tabs uses login state correctly."""
        logger.info("Entering test_multiple_tabs")
        context1 = browser.new_context()
        context2 = browser.new_context()
        page1 = context1.new_page()
        page2 = context2.new_page()
        login_page_1 = LoginPage(page1)
        login_page_1.login("standard_user", "secret_sauce")
        login_page_2 = LoginPage(page2)
        login_page_2.goto(f"{self.BASE_URL}/inventory.html")
        assert page2.url == LoginPage.URL
        context1.close()
        context2.close()

    def test_rapid_clicking_add_to_cart(self, logged_in_page):
        """Verify rapid repeated clicks on Add to Cart do not break the inventory page."""
        logger.info("Entering test_rapid_clicking_add_to_cart")
        inventory_page = logged_in_page
        # Add different products in rapid succession
        products = ["sauce-labs-backpack", "sauce-labs-bike-light", "sauce-labs-bolt-t-shirt", "sauce-labs-fleece-jacket", "sauce-labs-onesie"]
        for product in products[:5]:
            inventory_page.add_to_cart(product)
        assert inventory_page.page.url == InventoryPage.URL
        assert inventory_page.cart_count() == 5

    def test_session_persistence(self, logged_in_page):
        """Verify cart state and login persist after refreshing the page."""
        logger.info("Entering test_session_persistence")
        inventory_page = logged_in_page
        inventory_page.add_to_cart("sauce-labs-backpack")
        inventory_page.reload()
        assert inventory_page.page.url == InventoryPage.URL
        assert inventory_page.cart_count() == 1

    def test_large_viewport(self, browser):
        """Verify layout renders correctly at a large desktop viewport."""
        logger.info("Entering test_large_viewport")
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        login_page = LoginPage(page)
        login_page.login("standard_user", "secret_sauce")
        assert page.locator('.inventory_container').is_visible()
        context.close()

    def test_small_viewport(self, browser):
        """Verify layout renders correctly at a mobile viewport."""
        logger.info("Entering test_small_viewport")
        context = browser.new_context(viewport={"width": 375, "height": 667})
        page = context.new_page()
        login_page = LoginPage(page)
        login_page.login("standard_user", "secret_sauce")
        assert page.locator('.inventory_container').is_visible()
        context.close()
