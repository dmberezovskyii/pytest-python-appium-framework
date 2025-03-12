from typing import Literal

from locators.locators import Locators
from screens.base_screen import Screen


class MainScreen(Screen):
	
	def __init__(self, driver):
		super().__init__(driver)
		self.locators = Locators()
	
	def click_on_text_link(self):
		self.click(locator = self.locators.main_menu.TEXT_LINK)
	
	def tap_on_text_link(self):
		self.tap(locator = self.locators.main_menu.TEXT_LINK)
	
	def scroll_view_by_coordinates(self, direction: Literal['down', 'up'] = 'down'):
		self.tap(locator = self.locators.main_menu.VIEWS_LINK)
		self.scroll(directions = direction)
		
		