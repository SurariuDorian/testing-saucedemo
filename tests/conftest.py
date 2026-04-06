import pytest
import logging
import sys
from pathlib import Path

# Add the repo root to the Python path to allow absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.pages import InventoryPage, LoginPage

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Provide default browser context options for Playwright tests."""
    logger.info("Entering browser_context_args")
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture
def login_page(page):
    """Return a login page object for the SauceDemo login screen."""
    logger.info("Entering login_page")
    return LoginPage(page)


@pytest.fixture
def logged_in_page(login_page):
    """Return a page object that is already logged in as standard_user."""
    logger.info("Entering logged_in_page")
    login_page.navigate()
    return login_page.login("standard_user", "secret_sauce")


@pytest.fixture
def cart_with_items_page(logged_in_page):
    """Return a logged-in inventory page with two items already in the shopping cart."""
    logger.info("Entering cart_with_items_page")
    inventory = logged_in_page
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")
    return inventory
