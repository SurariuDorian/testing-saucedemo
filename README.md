# testing-saucedemo

Regression tests for the order placement process on https://www.saucedemo.com/

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Test Structure

The suite is implemented using a Page Object Model under `tests/pages`, with reusable fixtures defined in `tests/conftest.py`.

The test suite is organized into the following modules:

- `test_authentication.py`: Login/logout functionality
- `test_browsing.py`: Product browsing and sorting
- `test_cart.py`: Shopping cart operations
- `test_checkout.py`: Checkout process and validation
- `test_confirmation.py`: Order confirmation
- `test_order_placement.py`: End-to-end order placement workflows
- `test_edge_cases.py`: Edge cases and error scenarios
- `test_ui_ux.py`: UI/UX and accessibility tests

## Running Tests

Run all tests:
```bash
pytest
```

Run specific test module:
```bash
pytest tests/test_authentication.py
```

Run specific test:
```bash
pytest tests/test_checkout.py::TestCheckout::test_valid_checkout_information
```

Run tests with different browsers:
```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

Run tests in headed mode (visible browser):
```bash
pytest --headed
```

Use the built-in runner script for convenience:
```bash
python scripts/run_tests.py
```

## Test Coverage

The test suite covers:

- **Authentication**: All user types, valid/invalid logins, logout
- **Product Browsing**: Viewing products, sorting, product details
- **Shopping Cart**: Add/remove items, cart badge, empty cart
- **Checkout Process**: Form validation, order summary, completion
- **Order Confirmation**: Success page, navigation
- **Edge Cases**: Direct URL access, session management, browser navigation
- **UI/UX**: Responsive design, accessibility, visual consistency

## Fixtures

- `logged_in_page`: Provides a page already logged in as standard_user
- `cart_with_items_page`: Provides a page with items already in cart

## Test Data

- User credentials: standard_user, locked_out_user, problem_user, etc.
- Checkout information: Valid and invalid form data
- Product interactions: All 6 products in inventory

## Notes

- Tests use Playwright for browser automation
- Fixtures in conftest.py provide browser and page instances
- Tests are written in pytest style with parametrization for similar scenarios
- Some tests may need locator adjustments based on site updates 
