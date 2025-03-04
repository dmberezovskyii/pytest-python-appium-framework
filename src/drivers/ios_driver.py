from appium.webdriver import webdriver

from config import settings


class iOSDriver:
    @staticmethod
    def get_driver(platform: str):
        return webdriver.Remote(settings.APPIUM_SERVER, caps)
