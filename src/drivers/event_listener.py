import logging

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener

# TODO make logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AppEventListener(AbstractEventListener):
    """Custom Event Listener for Appium WebDriver."""

    def before_find(self, by, value, driver):
        logger.info(f"Looking for element: {by} -> {value}")

    def after_find(self, by, value, driver):
        logger.info(f"Found element: {by} -> {value}")

    def before_click(self, element, driver):
        logger.info(f"Before clicking: {element}")

    def after_click(self, element, driver):
        logger.info(f"Clicked on: {element}")

    def before_quit(self, driver):
        logger.info("Driver is about to quit.")

    def after_quit(self, driver):
        logger.info("Driver has quit.")

    def on_exception(self, exception, driver) -> None:
        logger.info(f"On exception")