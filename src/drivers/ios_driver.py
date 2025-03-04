from appium.webdriver import webdriver

from config import settings


class iOSDriver:
    @staticmethod
    def get_driver(platform: str):
        return settings.iOS.to_dict()
