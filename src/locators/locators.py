from appium.webdriver.common.appiumby import AppiumBy


class Locators:
	class main_menu:
		TEXT_LINK = (AppiumBy.ACCESSIBILITY_ID, 'Text')
		CONTENT_LINK = (AppiumBy.ACCESSIBILITY_ID, 'Content')
		VIEWS_LINK = (AppiumBy.ACCESSIBILITY_ID, 'Views')
		MENU_ELEMENTS = (AppiumBy.XPATH, '//android.widget.TextView')
	
	class views_menu:
		TEXT_FIELDS = (AppiumBy.ACCESSIBILITY_ID, 'TextFields')
		ANIMATION_LINK = (AppiumBy.ACCESSIBILITY_ID, 'Animation')
		GALLERY_LINK = (AppiumBy.ACCESSIBILITY_ID, 'Gallery')
		IMAGE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'ImageButton')
		
		class views_fields:
			HINT_INPUT = (AppiumBy.ACCESSIBILITY_ID, 'hint')