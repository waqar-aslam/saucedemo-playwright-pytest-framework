import base64
from pathlib import Path

import pytest
from playwright.sync_api import Playwright
from pytest_html import extras

from utils.data_loader import DataLoader
from utils.screenshot_helper import ScreenshotHelper


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Anchor relative report/artifact paths to the project root.

    pytest-html and pytest-playwright resolve these against the current
    working directory, so running pytest from a subfolder would scatter
    output. Runs before those plugins read the options.
    """
    for option in ("htmlpath", "output"):
        value = getattr(config.option, option, None)
        if value and not Path(value).is_absolute():
            setattr(config.option, option, str(config.rootpath / value))


@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    """--base-url if given, else base_url from config/urls.json.

    Overrides pytest-base-url's fixture. Deliberately not read from pytest.ini:
    the ini is skipped when pytest is launched from outside the project (e.g.
    an IDE opened on a parent folder), and pytest-base-url ignores the ini
    value on pytest-xdist workers.
    """
    return pytestconfig.getoption("base_url") or DataLoader.base_url()


@pytest.fixture(scope="session", autouse=True)
def use_data_test_attribute(playwright: Playwright):
    """SauceDemo tags elements with data-test, so get_by_test_id() uses it."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a test fails during its call phase
    and embed it in the pytest-html report."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")

    if page is None:
        return

    try:
        screenshot_path = ScreenshotHelper.capture(page, item.nodeid)
        print(f"Failure screenshot: {screenshot_path}")
    except Exception as error:
        print(f"Could not capture failure screenshot: {error}")
        return

    encoded = base64.b64encode(screenshot_path.read_bytes()).decode("ascii")
    report.extras = getattr(report, "extras", []) + [
        extras.png(encoded, name="Failure screenshot")
    ]
