import pytest

from drivers.driver_factory import Driver


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
        driver = Driver.get_driver(platform)
    except Exception as e:
        pytest.fail(f"Failed to initialize driver: {e}")

    yield driver
    if driver is not None:
        driver.quit()
