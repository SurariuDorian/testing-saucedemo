import pytest
import logging

from tests.pages import LoginPage

logger = logging.getLogger(__name__)

class TestAuthentication:
    """Authentication scenarios for SauceDemo login and logout workflows."""

    @pytest.mark.parametrize("username,password,expected_url", [
        ("standard_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
        ("problem_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
        ("performance_glitch_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
    ])
    def test_successful_login(self, login_page, username, password, expected_url):
        """Verify a valid user can log in and land on the inventory page."""
        logger.info("Entering test_successful_login")
        login_page.navigate()
        inventory_page = login_page.login(username, password)
        assert inventory_page.page.url == expected_url
        assert inventory_page.locator('.title').text_content() == "Products"

    def test_locked_out_user(self, login_page):
        """Verify a locked-out user receives the correct error message."""
        logger.info("Entering test_locked_out_user")
        login_page.navigate()
        login_page.attempt_login("locked_out_user", "secret_sauce")
        assert "sorry, this user has been locked out" in login_page.error_text().lower()

    def test_invalid_username(self, login_page):
        """Verify login fails when an invalid username is supplied."""
        logger.info("Entering test_invalid_username")
        login_page.navigate()
        login_page.attempt_login("invalid_user", "secret_sauce")
        assert "username and password do not match any user in this service" in login_page.error_text().lower()

    def test_invalid_password(self, login_page):
        """Verify login fails when an invalid password is supplied."""
        logger.info("Entering test_invalid_password")
        login_page.navigate()
        login_page.attempt_login("standard_user", "wrong_password")
        assert "username and password do not match any user in this service" in login_page.error_text().lower()

    def test_empty_credentials(self, login_page):
        """Verify the login form shows a required field error when submitted empty."""
        logger.info("Entering test_empty_credentials")
        login_page.navigate()
        login_page.submit()
        assert "username is required" in login_page.error_text().lower()

    def test_logout(self, logged_in_page):
        """Verify logging out returns the user to the login page and clears the session."""
        logger.info("Entering test_logout")
        inventory_page = logged_in_page
        login_page = inventory_page.logout()
        assert login_page.page.url == LoginPage.URL
        login_page.navigate()
        assert login_page.page.url == LoginPage.URL
