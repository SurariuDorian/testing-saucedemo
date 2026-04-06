import pytest
import logging

logger = logging.getLogger(__name__)

class TestBrowsing:
    """Product browsing and sorting scenarios for SauceDemo inventory."""

    def test_view_products(self, logged_in_page):
        """Verify all inventory products render with required details."""
        logger.info("Entering test_view_products")
        inventory_page = logged_in_page
        assert inventory_page.product_count() == 6
        for index in range(inventory_page.product_count()):
            product = inventory_page.locator(inventory_page.PRODUCT_ITEM).nth(index)
            assert product.locator(inventory_page.PRODUCT_IMAGE).is_visible()
            assert product.locator(inventory_page.PRODUCT_NAME).is_visible()
            assert product.locator(inventory_page.PRODUCT_PRICE).is_visible()
            assert product.locator('.inventory_item_desc').is_visible()

    @pytest.mark.parametrize("sort_option,expected_first,expected_last", [
        ("az", "Sauce Labs Backpack", "Test.allTheThings() T-Shirt (Red)"),
        ("za", "Test.allTheThings() T-Shirt (Red)", "Sauce Labs Backpack"),
        ("lohi", "Sauce Labs Onesie", "Sauce Labs Fleece Jacket"),
        ("hilo", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"),
    ])
    def test_sort_products(self, logged_in_page, sort_option, expected_first, expected_last):
        """Verify inventory sorting works for all supported options."""
        logger.info("Entering test_sort_products")
        inventory_page = logged_in_page
        inventory_page.sort_products(sort_option)
        titles = inventory_page.product_titles()
        assert titles[0] == expected_first
        assert titles[-1] == expected_last

    def test_product_details(self, logged_in_page):
        """Verify the product details page displays the correct information."""
        logger.info("Entering test_product_details")
        inventory_page = logged_in_page
        inventory_page.open_first_product()
        assert "inventory-item" in inventory_page.page.url
        assert inventory_page.locator('.inventory_details_name').is_visible()
        assert inventory_page.locator('.inventory_details_desc').is_visible()
        assert inventory_page.locator('.inventory_details_price').is_visible()
        inventory_page.click('[data-test="back-to-products"]')
        assert inventory_page.page.url == "https://www.saucedemo.com/inventory.html"
