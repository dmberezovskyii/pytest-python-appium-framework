from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium import webdriver

from config import settings
from drivers.android_driver import AndroidCaps
from drivers.ios_driver import IOSCaps
from utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO).get_instance()


class Driver:
    @staticmethod
    def get_driver(platform: str):
        """Get driver by platform, uses appropriate capabilities for Android or iOS."""
        caps = (
            AndroidCaps.get_caps()
            if platform.lower() == "android"
            else IOSCaps.get_caps()
        )

        if not caps:
            log.info(f"Capabilities not found for platform ❌: {platform}")
            raise ValueError(f"Capabilities not found for platform ❌: {platform}")

        if platform.lower() == "android":
            options = UiAutomator2Options().load_capabilities(caps)
            log.info(f"Capabilities: {options}")
        else:
            options = XCUITestOptions().load_capabilities(caps)
            log.info(f"Capabilities: {options}")

        driver = webdriver.Remote(settings.APPIUM_SERVER, options=options)
        return driver
