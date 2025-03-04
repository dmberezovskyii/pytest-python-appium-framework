from appium import webdriver

from config import settings
from src.drivers.android_driver import AndroidCaps


class Driver:
    @staticmethod
    def get_driver(platform: str):
        """Get driver by platform, uses appropriate capabilities for Android or iOS."""
        if platform.lower() == "android":
            caps = AndroidCaps.get_caps()
        else:
            caps = settings.iOS.to_dict()

        driver = webdriver.Remote(settings.APPIUM_SERVER, caps)
        return driver
