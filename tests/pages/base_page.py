from playwright.sync_api import Locator, Page
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object containing common browser operations."""

    def __init__(self, page: Page) -> None:
        """Initialize the base page with the Playwright page instance."""
        logger.info("Initializing BasePage")
        self.page = page

    def goto(self, url: str) -> None:
        """Navigate the browser to the specified URL."""
        logger.info("Navigating to %s", url)
        self.page.goto(url)

    def click(self, selector: str) -> None:
        """Click the element matching the provided selector."""
        logger.info("Clicking selector %s", selector)
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        """Fill the form field identified by selector with text."""
        logger.info("Filling selector %s with value", selector)
        self.page.fill(selector, value)

    def locator(self, selector: str) -> Locator:
        """Return a locator for the given selector."""
        logger.info("Getting locator for %s", selector)
        return self.page.locator(selector)

    def text_content(self, selector: str) -> str:
        """Return the text content for the given selector."""
        logger.info("Getting text content from %s", selector)
        return self.locator(selector).text_content() or ""

    def wait_for_url(self, url: str) -> None:
        """Wait until the current URL matches the expected value."""
        logger.info("Waiting for URL %s", url)
        self.page.wait_for_url(url)

    def is_visible(self, selector: str) -> bool:
        """Return whether the selector is visible in the page."""
        logger.info("Checking visibility for %s", selector)
        return self.locator(selector).is_visible()

    def select_option(self, selector: str, value: str) -> None:
        """Select the given option value in a dropdown."""
        logger.info("Selecting option %s in %s", value, selector)
        self.page.select_option(selector, value)

    def reload(self) -> None:
        """Reload the current page."""
        logger.info("Reloading page")
        self.page.reload()

    def go_back(self) -> None:
        """Navigate back in browser history."""
        logger.info("Going back in browser history")
        self.page.go_back()

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        logger.info("Going forward in browser history")
        self.page.go_forward()
