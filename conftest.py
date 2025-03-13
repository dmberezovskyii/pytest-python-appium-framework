import os

import pytest
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from drivers.driver_factory import Driver
from drivers.event_listener import AppEventListener


@pytest.hookimpl
def pytest_addoption(parser):
    """
    Adds command-line options for pytest.
    """
    parser.addoption(
        "--app", action="store", default="ios", help="Define App: ios or android"
    )
    parser.addoption(
        "--device", action="store", default="emulator", help="Define Device Type"
    )
    parser.addoption(
        "--platform", action="store", default="ios", help="Define Platform"
    )
    parser.addoption(
        "--env",
        action="store",
        default="stage",
        help="Define test environment (e.g., stage, prod)",
    )
    parser.addoption(
        "--listeners",
        action="store",
        default="events",
        help="Define listeners for the test run",
    )


@pytest.fixture(scope="session")
def app(request):
    """
    Retrieves the application type specified via the --app command-line option.
    """
    return request.config.getoption("--app")


@pytest.fixture(scope="session")
def device(request):
    """
    Retrieves the device type specified via the --device command-line option.
    """
    return request.config.getoption("--device")


@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform")

    try:
        e_listener = AppEventListener()
        driver = Driver.get_driver(platform)
        event_driver = EventFiringWebDriver(driver, e_listener)
    except Exception as e:
        pytest.fail(f"Failed to initialize driver: {e}")

    yield event_driver

    if event_driver is not None:
        event_driver.quit()


# def pytest_runtest_makereport(item, call):
#     """Capture screenshot on test failure."""
#     if call.excinfo is not None:
#         driver = item.funcargs.get("driver", None)
#
#         if driver is not None:
#             screenshot_dir = "reports/screenshots"
#             os.makedirs(
#                 screenshot_dir, exist_ok=True
#             )  # Create directory if it does not exist
#             screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
#
#             try:
#                 driver.save_screenshot(screenshot_path)
#                 # log.info(f"Screenshot saved to: {screenshot_path}")
#             except Exception as e:
#                 pass
#                 # log.error(f"Failed to save screenshot: {e}")
#         else:
#             pass
#             # log.error("Driver instance is not available for capturing screenshot.")
