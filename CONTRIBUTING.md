# Contributing to SauceDemo Testing

Thank you for your interest in contributing to the SauceDemo testing project! This document provides guidelines and information for contributors.

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the issue has already been reported in the [Issues](https://github.com/your-username/saucedemo-testing/issues) section
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Browser and OS information
   - Screenshots if applicable

### Suggesting Features

1. Check existing [Issues](https://github.com/your-username/saucedemo-testing/issues) for similar suggestions
2. Create a new issue with:
   - Clear description of the proposed feature
   - Use case and benefits
   - Any relevant mockups or examples

### Contributing Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run the test suite: `pytest`
   or `python scripts/run_tests.py`
5. Ensure all tests pass
6. Commit your changes: `git commit -m "Add your message"`
7. Push to your branch: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- Playwright

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/saucedemo-testing.git
   cd saucedemo-testing
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/test_authentication.py

# Run with coverage
pytest --cov=tests

# Run in headed mode (visible browser)
pytest --headed
```

## Code Style

This project follows PEP 8 style guidelines. Please ensure your code:

- Uses 4 spaces for indentation
- Has descriptive variable and function names
- Includes docstrings for functions and classes
- Follows the existing code patterns

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality. Install them with:

```bash
pip install pre-commit
pre-commit install
```

## Testing Guidelines

### Writing Tests

- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Use fixtures for common setup code
- Parametrize tests when testing similar scenarios
- Include assertions for both positive and negative cases

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_authentication.py   # Authentication tests
├── test_browsing.py         # Product browsing tests
├── test_cart.py            # Shopping cart tests
├── test_checkout.py        # Checkout process tests
├── test_confirmation.py    # Order confirmation tests
├── test_order_placement.py  # End-to-end order placement workflows
├── test_edge_cases.py      # Edge cases and error scenarios
└── test_ui_ux.py           # UI/UX tests
```

### Test Data

- Use realistic test data
- Avoid hardcoding sensitive information
- Use fixtures for common test data

## Documentation

- Update README.md for any new features
- Add docstrings to new functions and classes
- Update this CONTRIBUTING.md if processes change

## Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

## Pull Request Process

1. Ensure your PR has a clear title and description
2. Reference any related issues
3. Ensure all CI checks pass
4. Request review from maintainers
5. Address any feedback
6. Once approved, your PR will be merged

## Questions?

If you have questions about contributing, please create an issue or contact the maintainers.

Thank you for contributing to the SauceDemo testing project! 🚀