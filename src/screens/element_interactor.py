import time
from enum import Enum
from typing import Tuple, Optional, Literal, List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    ElementNotVisibleException,
    NoSuchElementException,
)

Locator = Tuple[str, str]


class WaitType(Enum):
    """
    Enumeration for different wait durations used in WebDriverWait.
    """

    DEFAULT = 30
    SHORT = 5
    LONG = 60
    FLUENT = 10


class ElementInteractor:
    """
    A utility class for interacting with web elements and handling waits.

    This class provides various methods for waiting for elements, checking their visibility,
    existence
    """

    def __init__(self, driver):
        """
        Initializes the ElementInteractor with a WebDriver instance and predefined waiters.

        :param driver: The Selenium WebDriver instance to interact with.
        :type driver: WebDriver
        """
        self.driver = driver
        self.waiters = {
            WaitType.DEFAULT: WebDriverWait(driver, WaitType.DEFAULT.value),
            WaitType.SHORT: WebDriverWait(driver, WaitType.SHORT.value),
            WaitType.LONG: WebDriverWait(driver, WaitType.LONG.value),
            WaitType.FLUENT: WebDriverWait(
                driver,
                WaitType.FLUENT.value,
                poll_frequency=1,
                ignored_exceptions=[ElementNotVisibleException],
            ),
        }

    def _get_waiter(self, wait_type: Optional[WaitType] = None) -> WebDriverWait:
        """
        Returns the appropriate WebDriverWait instance based on the specified wait type.

        :param wait_type: The type of wait (default is `WaitType.DEFAULT`).
        :type wait_type: Optional[WaitType]

        :return: The WebDriverWait instance for the specified wait type.
        :rtype: WebDriverWait
        """
        return self.waiters.get(wait_type, self.waiters[WaitType.DEFAULT])

    def wait_for(
        self,
        locator: Locator,
        condition: Literal["clickable", "visible", "present"] = "visible",
        waiter: Optional[WebDriverWait] = None,
    ) -> WebElement:
        """
        Waits for an element to meet the specified condition.

        :param locator: A tuple containing the strategy and value of the element locator.
        :param condition: The condition to wait for ("clickable", "visible", or "present").
        :param waiter: A custom WebDriverWait instance. Defaults to `None`, which uses the default waiter.

        :return: The located web element once the condition is satisfied.
        """
        waiter = waiter or self._get_waiter()
        conditions = {
            "clickable": ec.element_to_be_clickable(locator),
            "visible": ec.visibility_of_element_located(locator),
            "present": ec.presence_of_element_located(locator),
        }

        if condition not in conditions:
            raise ValueError(f"Unknown condition: {condition}")

        try:
            return waiter.until(conditions[condition])
        except TimeoutException as e:
            raise TimeoutException(
                f"Condition '{condition}' failed for element {locator} "
                f"after {waiter._timeout} seconds"
            ) from e

    def elements(
        self,
        locator: Locator,
        n: int = 3,
        condition: Literal["clickable", "visible", "present"] = "visible",
        wait_type: Optional[WaitType] = WaitType.DEFAULT,
    ) -> List[WebElement]:
        """
        Attempts to locate a list of elements by polling a maximum of 'n' times.

        :param locator: A tuple containing the strategy and value of the element locator.
        :param n: The maximum number of attempts to find the elements. Default is 3.
        :param condition: The condition to wait for ("clickable", "visible", or "present").
        :param wait_type: The wait type to use for polling. Defaults to `WaitType.DEFAULT`.

        :return: A list of located web elements that match the condition.
        """
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
            except Exception:
                if attempt == n:
                    raise

    def _assert_element_displayed(self, element: WebElement, expected: bool) -> None:
        """
        Asserts that the element's displayed status matches the expected value.

        :param element: The web element to check.
        :param expected: The expected visibility status of the element (True or False).

        :raises AssertionError: If the element's visibility does not match the expected value.
        """
        assert element.is_displayed() == expected

    def _check_elements_displayed(
        self, elements: List[WebElement], expected: bool, index: Optional[int] = None
    ) -> bool:
        """
        Checks if the elements are displayed and if applicable, checks a specific element by index.

        :param elements: The list of web elements to check.
        :param expected: The expected visibility status of the elements (True or False).
        :param index: The index of the specific element to check. If `None`, all elements are checked.
        :return: True if the element(s) are displayed with the expected status, otherwise False.
        """
        if index is None:
            return all(e.is_displayed() == expected for e in elements)
        return elements[index].is_displayed() == expected

    def is_displayed(
        self,
        locator: Locator,
        expected: bool = True,
        n: int = 3,
        condition: Literal["clickable", "visible", "present"] = "visible",
        wait_type: Optional[WaitType] = WaitType.DEFAULT,
        **kwargs,
    ) -> None:
        """
        Polls for an element to be displayed or not, and asserts the visibility.

        :param locator: A tuple containing the strategy and value of the element locator.
        :param expected: The expected visibility status of the element (True or False).
        :param n: The maximum number of attempts to check visibility. Defaults to 3.
        :param condition: The condition to wait for ("clickable", "visible", or "present").
        :param wait_type: The wait type to use for polling. Defaults to `WaitType.DEFAULT`.

        :raises AssertionError: If the element's visibility does not match the expected value after polling.
        """
        for _ in range(n):
            try:
                element = self.wait_for(
                    locator, condition=condition, waiter=self._get_waiter(wait_type)
                )
                self._assert_element_displayed(element, expected)
                break
            except Exception:
                time.sleep(0.5)
                if _ == n - 1:
                    assert False == expected

    def is_exist(
        self,
        locator: Locator,
        expected: bool = True,
        n: int = 3,
        condition: Literal["clickable", "visible", "present"] = "visible",
        wait_type: Optional[WaitType] = WaitType.DEFAULT,
        **kwargs,
    ) -> bool:
        """
        Polls for an element's existence and checks if it meets the expected visibility status.

        :param locator: A tuple containing the strategy and value of the element locator.
        :param expected: The expected existence status of the element (True or False).
        :param n: The maximum number of attempts to check existence. Defaults to 3.
        :param condition: The condition to wait for ("clickable", "visible", or "present").
        :param wait_type: The wait type to use for polling. Defaults to `WaitType.DEFAULT`.
        :param **kwargs: Additional keyword arguments, such as `index` for checking a specific element in a list.

        :return: `True` if the element(s) exist and match the expected visibility status, otherwise `False`.
        :rtype: bool
        """
        for _ in range(n):
            try:
                elements = self.wait_for(
                    locator, condition=condition, waiter=self._get_waiter(wait_type)
                )
                if isinstance(elements, list) and self._check_elements_displayed(
                    elements, expected, kwargs.get("index")
                ):
                    return True
            except Exception:
                if _ == n - 1:
                    return False
