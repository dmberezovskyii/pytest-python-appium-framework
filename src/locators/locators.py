from appium.webdriver.common.appiumby import AppiumBy


class Common:
	text_link = (AppiumBy.ACCESSIBILITY_ID, 'Text')
	content_link = (AppiumBy.ACCESSIBILITY_ID, 'Content')
	menu_elements = (AppiumBy.XPATH, '//android.widget.TextView')