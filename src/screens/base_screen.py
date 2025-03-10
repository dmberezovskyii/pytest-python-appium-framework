import time
from typing import Tuple, Literal

from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_actions import PointerActions

from screens.element_interactor import ElementInteractor
from appium.webdriver.extensions.action_helpers import ActionHelpers, ActionChains


Locator = Tuple[str, str]


class Screen(ElementInteractor):
    def __init__(self, driver):
        super().__init__(driver)

    def click(
        self,
        locator: Locator,
        condition: Literal["clickable", "visible", "present"] = "clickable",
    ):
        element = self.element(locator, condition=condition)
        element.click()

    def tap(self, locator, **kwargs):
        """Taps on an element using ActionHelpers."""
        try:
            element = self.element(locator, condition="clickable", **kwargs)
            location = element.location
            size = element.size
            x = location["x"] + size["width"] // 2
            y = location["y"] + size["height"] // 2
            self.driver.tap([(x, y)])
        except Exception as e:
            print(f"Error during tap action: {e}")

    def swipe(
        self,
        relative_start_x: float,
        relative_start_y: float,
        relative_end_x: float,
        relative_end_y: float,
        duration_ms: int = 200,
    ) -> None:
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        start_x = int(width * relative_start_x)
        start_y = int(height * relative_start_y)
        end_x = int(width * relative_end_x)
        end_y = int(height * relative_end_y)
        self.driver.swipe(
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            duration_ms=duration_ms,
        )

    def type(self, locator: Locator, text: str):
        element = self.element(locator)
        element.send_keys(text)

    def double_tap(
        self,
        locator: Locator,
        condition: Literal["clickable", "visible", "present"] = "clickable",
        **kwargs,
    ):
        """Double taps on an element."""
        try:
            element = self.element(locator, condition=condition, **kwargs)
            action = ActionHelpers()
            action.double_tap(element).perform()
        except Exception as e:
            print(f"Error during double tap action: {e}")

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
