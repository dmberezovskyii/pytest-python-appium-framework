from typing import Literal

from locators.locators import Locators
from screens.base_screen import Screen
from utils.logger import log


class MainScreen(Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = Locators()

    def click_on_text_link(self):
        """Click on text link"""
        self.click(locator=self.locators.main_menu.TEXT_LINK)

    def tap_on_text_link(self):
        """Tap on text link"""
        self.tap(locator=self.locators.main_menu.TEXT_LINK)

    def scroll_view_by_coordinates(self, direction: Literal["down", "up"] = "down"):
        """Scroll by coordinates"""
        self.tap(locator=self.locators.main_menu.VIEWS_LINK)
        self.scroll(directions=direction)

    def scroll_to_image_button(self):
        """Scroll to image button"""
        self.tap(locator=self.locators.main_menu.VIEWS_LINK)
        self.scroll_to_element(
            from_el=self.locators.views_menu.ANIMATION_LINK,
            destination_el=self.locators.views_menu.IMAGE_BUTTON,
        )

    def scroll_until_text_field_visible(self):
        """Scroll until element visible"""
        self.tap(locator=self.locators.main_menu.VIEWS_LINK)
        self.scroll_until_element_visible(
            destination_el=self.locators.views_menu.TEXT_FIELDS
        )

    def swipe_tab(self):
        """Move to Scrollable tab and swipe left"""
        self.tap(locator=self.locators.main_menu.VIEWS_LINK)
        self.scroll_until_element_visible(
            destination_el=self.locators.views_menu.TABS_LINK
        )
        self.tap(locator=self.locators.views_menu.TABS_LINK)
        self.tap(locator=self.locators.views_menu.tabs_fields.SCROLLABLE_LINK)
        self.swipe_to_delete(
            locator=self.locators.views_menu.tabs_fields.SCROLLABLE_TAB,
            direction="left",
        )

    def type_text(self, text):
        """Type text to field with HINT"""
        self.tap(locator=self.locators.main_menu.VIEWS_LINK)
        self.scroll_until_element_visible(
            destination_el=self.locators.views_menu.TEXT_FIELDS
        )
        self.tap(locator=self.locators.views_menu.TEXT_FIELDS)
        self.click(locator=self.locators.views_menu.text_fields.HINT_INPUT)
        self.type(locator=self.locators.views_menu.text_fields.HINT_INPUT, text=text)

    def double_tap_on_views_link(self):
        """Double tap"""
        self.double_tap(locator=self.locators.main_menu.VIEWS_LINK)
