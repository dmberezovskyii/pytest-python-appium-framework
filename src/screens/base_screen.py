import time
from typing import Tuple, Literal, Optional

from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from selenium.webdriver.common.actions.pointer_input import PointerInput

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

    def tap(self, locator: Locator, duration: float = 500, **kwargs):
        """Taps on an element using ActionHelpers.
        Taps on an particular place with up to five fingers, holding for a
        certain duration

        :param locator: locator of an element
        :param duration: length of time to tap, in ms"""
        try:
            element = self.element(locator, condition="clickable", **kwargs)
            location = element.location
            size = element.size
            x = location["x"] + size["width"] // 2
            y = location["y"] + size["height"] // 2
            self.driver.tap([(x, y)], duration=duration)
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
        size = self.get_screen_size()
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

    def scroll(
        self,
        directions: Literal["down", "up"] = "down",
        start_ratio: float = 0.7,
        end_ratio: float = 0.3,
    ):
        """
            Scrolls down the screen with customizable scroll size.

            :param directions: up or down:
            :param start_ratio:  Percentage (0-1) from where the scroll starts
            :type end_ratio: Percentage (0-1) where the scroll ends.
            USAGE:
        DOWN example
        start_y = int(height * 0.7)
        end_y = int(height * 0.3)
        UP example
        start_y = int(height * 0.3)
        end_y = int(height * 0.7)
        """
        size = self.get_screen_size()
        width = size["width"]
        height = size["height"]
        start_x = width // 2
        if directions == "down":
            start_y = int(height * start_ratio)
            end_y = int(height * end_ratio)
        elif directions == "up":
            start_y = int(height * end_ratio)
            end_y = int(height * start_ratio)
        else:
            raise ValueError("Direction must be 'down' or 'up'")

        self.scroll_by_coordinates(start_x, start_y, start_x, end_y)

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
            # TODO
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
