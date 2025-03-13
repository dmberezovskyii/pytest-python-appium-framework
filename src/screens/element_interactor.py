from enum import Enum
from typing import Tuple, Optional, Literal, List, cast
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

Locator = Tuple[str, str]
type Condition = Literal["clickable", "visible", "present"]


class WaitType(Enum):
    DEFAULT = 30
    SHORT = 5
    LONG = 60
    FLUENT = 10


class ElementInteractor:
    def __init__(self, driver):
        self.driver = driver
        self.waiters = {
            wait_type: WebDriverWait(driver, wait_type.value)
            for wait_type in WaitType
            if wait_type != WaitType.FLUENT
        }
        self.waiters[WaitType.FLUENT] = WebDriverWait(
            driver, WaitType.FLUENT.value, poll_frequency=1
        )
    
    def _get_waiter(self, wait_type: Optional[WaitType] = None) -> WebDriverWait:
        """Returns the appropriate waiter based on the given wait_type."""
        return self.waiters.get(wait_type, self.waiters[WaitType.DEFAULT])

    def wait_for(
        self,
        locator: Locator,
        condition: Condition = "visible",
        waiter: Optional[WebDriverWait] = None,
    ) -> WebElement:
        waiter = waiter or self._get_waiter()
        conditions = {
            "clickable": EC.element_to_be_clickable(locator),
            "visible": EC.visibility_of_element_located(locator),
            "present": EC.presence_of_element_located(locator),
        }
        if condition not in conditions:
            raise ValueError(f"Unknown condition: {condition}")
        try:
            return waiter.until(conditions[condition])
        except TimeoutException as e:
            raise TimeoutException(
                f"Condition '{condition}' failed for element {locator} after {waiter._timeout} seconds"
            ) from e

    def element(
        self,
        locator: Locator,
        n: int = 3,
        condition: Condition = "visible",
        wait_type: Optional[WaitType] = WaitType.DEFAULT,
    ):
        for attempt in range(1, n + 1):
            try:
                self.wait_for(
                    locator, condition=condition, waiter=self._get_waiter(wait_type)
                )
                return self.driver.find_element(*locator)
            except NoSuchElementException:
                if attempt == n:
                    raise NoSuchElementException(
                        f"Could not locate element with value: {locator}"
                    )

    def elements(
        self,
        locator: Locator,
        n: int = 3,
        condition: Condition = "visible",
        wait_type: Optional[WaitType] = WaitType.DEFAULT,
    ) -> List[WebElement]:
        for attempt in range(1, n + 1):
            try:
                self.wait_for(
                    locator, condition=condition, waiter=self._get_waiter(wait_type)
                )
                return self.driver.find_elements(*locator)
            except NoSuchElementException:
                if attempt == n:
                    raise NoSuchElementException(
                        f"Could not locate element list with value: {locator}"
                    )

    def is_displayed(
        self,
        locator: Locator,
        expected: bool = True,
        n: int = 3,
        condition: Condition = "visible",
        wait_type: Optional[WaitType] = None,
    ) -> None:
        wait_type = wait_type or WaitType.DEFAULT
        for _ in range(n):
            try:
                element = self.wait_for(
                    locator, condition=condition, waiter=self._get_waiter(wait_type)
                )
                assert element.is_displayed() == expected
                return
            except Exception:
                time.sleep(0.5)
        if expected:  # Assert if the element is expected to be displayed but isn't
            raise AssertionError(f"Element {locator} was not displayed as expected.")
        else:  # Assert if the element should not be displayed but is
            raise AssertionError(
                f"Element {locator} was displayed when it shouldn't be."
            )

    def is_exist(
        self,
        locator: Locator,
        expected: bool = True,
        n: int = 3,
        condition: Condition = "visible",
        wait_type: Optional[WaitType] = WaitType.SHORT,
        retry_delay: float = 0.5,
    ) -> bool:
        """
        Checks if an element exists on the screen within a specified number of retries.

        :param retry_delay: delay between retry
        :param locator: The locator tuple (strategy, value) used to find the element.
        :param expected: Determines whether the element should exist (True) or not (False).
        :param n: The number of attempts to check for the element before returning a result.
        :param condition: The condition to check for the element's existence.
                - "clickable": Ensures the element is interactable.
                - "visible": Ensures the element is visible on the page.
                - "present": Ensures the element exists in the DOM (even if not visible).
        :param wait_type: Specifies the wait strategy (default is WaitType.DEFAULT).
        :return: True if the element matches the expected state, False otherwise.
        :rtype: bool


        **Usage Example:**

         screen.is_exist(("id", "login-button"))
        True

         screen.is_exist(("id", "error-popup"), expected=False)
        True
        """
        for _ in range(n):
            try:
                element = self.element(
                    locator, n=1, condition=condition, wait_type=wait_type
                )
                return element.is_displayed() == expected
            except (NoSuchElementException, TimeoutException):
                if not expected:
                    return True
            except Exception as e:
                print(f"Unexpected error in is_exist: {e}")
            time.sleep(retry_delay)
        return not expected

    def scroll_by_coordinates(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: Optional[int] = None,
    ):
        """Scrolls from one set of coordinates to another.

        Args:
                start_x: X coordinate to start scrolling from.
                start_y: Y coordinate to start scrolling from.
                end_x: X coordinate to scroll to.
                end_y: Y coordinate to scroll to.
                duration: Defines speed of scroll action. Default is 700 ms.
        """
        if duration is None:
            duration = 700

        touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionChains(self.driver)

        actions.w3c_actions = ActionBuilder(self.driver, mouse=touch_input)
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=touch_input, duration=duration
        )

        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()

        actions.perform()
