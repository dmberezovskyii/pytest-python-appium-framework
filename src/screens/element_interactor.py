from enum import Enum
from typing import Tuple, Optional, Literal, List
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

Locator = Tuple[str, str]


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
        return self.waiters.get(wait_type, self.waiters[WaitType.DEFAULT])

    def wait_for(
        self,
        locator: Locator,
        condition: Literal["clickable", "visible", "present"] = "visible",
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
        condition: Literal["clickable", "visible", "present"] = "visible",
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
        condition: Literal["clickable", "visible", "present"] = "visible",
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
        condition: Literal["clickable", "visible", "present"] = "visible",
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
        condition: Literal["clickable", "visible", "present"] = "visible",
        wait_type: Optional[WaitType] = WaitType.DEFAULT,
    ) -> bool:
        for _ in range(n):
            try:
                element = self.element(
                    locator, n=1, condition=condition, wait_type=wait_type
                )
                return element.is_displayed() == expected
            except NoSuchElementException:
                if not expected:
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return not expected
