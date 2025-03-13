import logging

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener

from utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO).get_instance()


class AppEventListener(AbstractEventListener):
    """Custom Event Listener for Appium WebDriver."""

    # def before_find(self, by, value, driver):
    #     logger.info(f"Looking for element: {by} -> {value}")

    def after_find(self, by, value, driver):
        log.info(f"Found element: {by} -> {value}")

    # def before_click(self, element, driver):
    #     logger.info(f"Before clicking: {element}")

    def after_click(self, element, driver):
        log.info(f"Clicked on: {element}")

    def after_quit(self, driver):
        log.info("Driver has quit.")

    def on_exception(self, exception, driver) -> None:
        log.info(f"On exception")
