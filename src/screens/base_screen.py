import time
from typing import Tuple, Literal

from screens.element_interactor import ElementInteractor


Locator = Tuple[str, str]
type Condition = Literal["clickable", "visible", "present"]
type Direction = Literal["down", "up"]


class Screen(ElementInteractor):
    def __init__(self, driver):
        super().__init__(driver)

    def click(self, locator: Locator, condition: Condition = "clickable"):
        element = self.element(locator, condition=condition)
        element.click()

    def tap(self, locator: Locator, duration: float = 500, **kwargs):
        """Taps on an element using ActionHelpers.
        Taps on a particular place with up to five fingers, holding for a
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
        directions: Direction = "down",
        start_ratio: float = 0.7,
        end_ratio: float = 0.3,
    ):
        """
            Scrolls down/up the screen with customizable scroll size.

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

    def scroll_to_element(
        self, from_el: Locator, destination_el: Locator, duration: [int] = 500
    ):
        """Scrolls to the destination element(Both elements must be located(visible)).

        :param from_el: Locator of the element to start scrolling from.
        :param destination_el: Locator of the target element to scroll to.
        :param duration: Optional duration for each scroll.
        """
        from_element = self.element(from_el)
        to_element = self.element(destination_el)

        self.driver.scroll(to_element, from_element, duration=duration)

    def scroll_until_element_visible(
        self,
        destination_el: Locator,
        directions: Direction = "down",
        start_ratio: float = 0.6,
        end_ratio: float = 0.3,
        retries: int = 1,
    ):
        while self.is_exist(destination_el, expected=False, n=retries):
            self.scroll(
                directions=directions, start_ratio=start_ratio, end_ratio=end_ratio
            )

    def type(self, locator: Locator, text: str):
        element = self.element(locator)
        element.send_keys(text)

    def double_tap(
        self, locator: Locator, condition: Condition = "clickable", **kwargs
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
