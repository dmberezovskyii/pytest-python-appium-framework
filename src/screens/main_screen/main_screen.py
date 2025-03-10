from locators.locators import Common
from screens.base_screen import Screen


class MainScreen(Screen):
	
	def __init__(self, driver):
		super().__init__(driver)
	
	def click_on_text_link(self):
		self.click(locator = Common.text_link)
	
	def tap_on_text_link(self):
		self.tap(locator = Common.text_link)