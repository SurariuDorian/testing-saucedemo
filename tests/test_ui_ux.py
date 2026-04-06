import pytest
import logging

from tests.pages import InventoryPage, LoginPage

logger = logging.getLogger(__name__)

class TestUIUX:
    """User interface and experience tests for SauceDemo."""

    def test_responsive_design_desktop(self, browser):
        """Verify SauceDemo renders correctly at a desktop viewport."""
        logger.info("Entering test_responsive_design_desktop")
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.enter_credentials("standard_user", "secret_sauce")
        login_page.submit()
        login_page.wait_for_url(InventoryPage.URL)
        assert page.locator('.header_container').is_visible()
        assert page.locator('.inventory_container').is_visible()
        context.close()

    def test_responsive_design_mobile(self, browser):
        """Verify SauceDemo renders correctly on a mobile viewport."""
        logger.info("Entering test_responsive_design_mobile")
        context = browser.new_context(viewport={"width": 375, "height": 667})
        page = context.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.enter_credentials("standard_user", "secret_sauce")
        login_page.submit()
        login_page.wait_for_url(InventoryPage.URL)
        assert page.locator('.header_container').is_visible()
        assert page.locator('.inventory_container').is_visible()
        context.close()

    def test_accessibility_login_form(self, page):
        """Verify the login form includes proper placeholders and actionable controls."""
        logger.info("Entering test_accessibility_login_form")
        login_page = LoginPage(page)
        login_page.navigate()
        username_input = login_page.locator(LoginPage.USERNAME)
        password_input = login_page.locator(LoginPage.PASSWORD)
        assert username_input.get_attribute('placeholder') == "Username"
        assert password_input.get_attribute('placeholder') == "Password"
        login_btn = login_page.locator(LoginPage.LOGIN_BUTTON)
        assert login_btn.is_visible()

    def test_visual_consistency(self, logged_in_page):
        """Verify inventory page layout remains consistent across product cards."""
        logger.info("Entering test_visual_consistency")
        inventory_page = logged_in_page
        assert inventory_page.locator('.header_container').is_visible()
        assert inventory_page.locator('.footer').is_visible()
        product_count = inventory_page.product_count()
        for index in range(min(3, product_count)):
            product = inventory_page.locator(inventory_page.PRODUCT_ITEM).nth(index)
            assert product.locator(inventory_page.PRODUCT_IMAGE).is_visible()
            assert product.locator(inventory_page.PRODUCT_NAME).is_visible()
            assert product.locator(inventory_page.PRODUCT_PRICE).is_visible()

    def test_keyboard_navigation(self, page):
        """Verify keyboard tabbing moves focus through the login page elements."""
        logger.info("Entering test_keyboard_navigation")
        login_page = LoginPage(page)
        login_page.navigate()
        page.keyboard.press('Tab')
        assert page.locator(LoginPage.USERNAME).evaluate('el => el === document.activeElement')
        page.keyboard.press('Tab')
        assert page.locator(LoginPage.PASSWORD).evaluate('el => el === document.activeElement')
        page.keyboard.press('Tab')
        assert page.locator(LoginPage.LOGIN_BUTTON).evaluate('el => el === document.activeElement')

    def test_error_message_visibility(self, page):
        """Verify login form error messages appear when submitting invalid credentials."""
        logger.info("Entering test_error_message_visibility")
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.submit()
        error = login_page.locator(LoginPage.ERROR_MESSAGE)
        assert error.is_visible()
        assert "required" in error.text_content().lower()

    def test_loading_states(self, logged_in_page):
        """Verify there are no stuck loading indicators on the main inventory page."""
        logger.info("Entering test_loading_states")
        inventory_page = logged_in_page
        assert not inventory_page.locator('.loading').is_visible()
        assert inventory_page.locator('.inventory_container').is_visible()

    def test_image_loading(self, logged_in_page):
        """Verify all product images have loaded successfully."""
        logger.info("Entering test_image_loading")
        inventory_page = logged_in_page
        images = inventory_page.locator('.inventory_item_img img')
        for index in range(images.count()):
            img = images.nth(index)
            assert img.is_visible()
            assert img.evaluate('img => img.naturalWidth > 0')
