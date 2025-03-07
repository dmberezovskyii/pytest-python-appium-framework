import time
from typing import Tuple

from screens.element_interactor import ElementInteractor

Locator = Tuple[str, str]


class Screen(ElementInteractor):
    def __init__(self, driver):
        super().__init__(driver)

    def click(self):
        pass

    def tap(self):
        pass
    
    def tap_by_coordinates(self):
        pass

    def swipe(self):
        pass

    def type(self):
        pass

    def double_tap(self):
        pass

    def long_press(self):
        pass

    @staticmethod
    def sleep(kwargs):
        try:
            time.sleep(kwargs["sleep"])
        except KeyError:
            pass

    def get_screen_size(self):
        return self.driver.get_window_size()
    
    def back(self):
        self.driver.back()

    def close(self):
        self.driver.close_app()

    def reset(self):
        self.driver.reset()

    def launch_app(self):
        self.driver.launch_app()