#!/usr/bin/env python3
"""
Test Runner Script for SauceDemo Testing Suite

This script provides a convenient way to run tests with various options
and generate reports.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

def run_command(cmd: list, description: str) -> int:
    """Run a command and return the exit code."""
    logger.info("Entering run_command")
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*50)

    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return e.returncode


def main():
    """Parse runner options and execute the SauceDemo test suite."""
    logger.info("Entering main")
    parser = argparse.ArgumentParser(
        description="SauceDemo Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_tests.py                    # Run all tests
  python scripts/run_tests.py --browser firefox  # Run with Firefox
  python scripts/run_tests.py --coverage         # Run with coverage
  python scripts/run_tests.py --module auth      # Run auth tests only
  python scripts/run_tests.py --headed           # Run in headed mode
        """
    )

    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser to use for testing (default: chromium)"
    )

    parser.add_argument(
        "--module",
        choices=["auth", "browsing", "cart", "checkout", "confirmation", "edge", "ui"],
        help="Run tests for specific module only"
    )

    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report"
    )

    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run tests in headed mode (visible browser)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate HTML test report"
    )

    args = parser.parse_args()

    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]

    # Add browser
    cmd.extend(["--browser", args.browser])

    # Add module filter
    if args.module:
        module_map = {
            "auth": "test_authentication.py",
            "browsing": "test_browsing.py",
            "cart": "test_cart.py",
            "checkout": "test_checkout.py",
            "confirmation": "test_confirmation.py",
            "edge": "test_edge_cases.py",
            "ui": "test_ui_ux.py"
        }
        cmd.append(f"tests/{module_map[args.module]}")

    # Add coverage
    if args.coverage:
        cmd.extend([
            "--cov=tests",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])

    # Add headed mode
    if args.headed:
        cmd.append("--headed")

    # Add verbose
    if args.verbose:
        cmd.append("-v")

    # Add HTML report
    if args.report:
        cmd.extend([
            "--html=test-results/report.html",
            "--self-contained-html"
        ])

    # Run the tests
    exit_code = run_command(cmd, f"SauceDemo Tests (Browser: {args.browser})")

    if exit_code == 0:
        print("\n✅ All tests passed!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/")
        if args.report:
            print("📄 HTML report generated in test-results/report.html")
    else:
        print(f"\n❌ Tests failed with exit code: {exit_code}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
