from __future__ import annotations

import logging

from .base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page object for the SauceDemo login screen."""

    URL = "https://www.saucedemo.com/"
    USERNAME = '[data-test="username"]'
    PASSWORD = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'

    def navigate(self) -> None:
        """Navigate to the SauceDemo login page."""
        logger.info("Navigating to login page")
        self.goto(self.URL)

    def enter_credentials(self, username: str, password: str) -> None:
        """Fill in the login credentials on the login page."""
        logger.info("Entering credentials for user %s", username)
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)

    def submit(self) -> None:
        """Submit the login form."""
        logger.info("Submitting login form")
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> "InventoryPage":
        """Perform a login and return the inventory page after successful authentication."""
        from .inventory_page import InventoryPage

        logger.info("Logging in user %s", username)
        self.navigate()
        self.enter_credentials(username, password)
        self.submit()
        self.wait_for_url(InventoryPage.URL)
        return InventoryPage(self.page)

    def attempt_login(self, username: str, password: str) -> "LoginPage":
        """Attempt login without waiting for a successful redirect."""
        logger.info("Attempting login for user %s", username)
        self.enter_credentials(username, password)
        self.submit()
        return self

    def error_text(self) -> str:
        """Return the login error message text."""
        logger.info("Fetching login error text")
        return self.text_content(self.ERROR_MESSAGE)
