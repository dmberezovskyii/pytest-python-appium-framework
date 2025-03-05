from appium import webdriver

from config import settings
from src.drivers.android_driver import AndroidCaps
from src.drivers.ios_driver import iOSCaps


class Driver:
    @staticmethod
    def get_driver(platform: str):
        """Get driver by platform, uses appropriate capabilities for Android or iOS."""
        if platform.lower() == "android":
            caps = AndroidCaps.get_caps()
        else:
            caps = iOSCaps.get_caps()

        driver = webdriver.Remote(settings.APPIUM_SERVER, caps)
        return driver
