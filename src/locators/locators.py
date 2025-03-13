from appium.webdriver.common.appiumby import AppiumBy


class Locators:
    class main_menu:
        TEXT_LINK = (AppiumBy.ACCESSIBILITY_ID, "Text")
        CONTENT_LINK = (AppiumBy.ACCESSIBILITY_ID, "Content")
        VIEWS_LINK = (AppiumBy.ACCESSIBILITY_ID, "Views")
        MENU_ELEMENTS = (AppiumBy.XPATH, "//android.widget.TextView")

    class views_menu:
        TEXT_FIELDS = (AppiumBy.ACCESSIBILITY_ID, "TextFields")
        ANIMATION_LINK = (AppiumBy.ACCESSIBILITY_ID, "Animation")
        GALLERY_LINK = (AppiumBy.ACCESSIBILITY_ID, "Gallery")
        IMAGE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "ImageButton")
        TABS_LINK = (AppiumBy.ACCESSIBILITY_ID, "Tabs")

        class text_fields:
            HINT_INPUT = (AppiumBy.ID, "io.appium.android.apis:id/edit")

        class tabs_fields:
            SCROLLABLE_LINK = (AppiumBy.ACCESSIBILITY_ID, "5. Scrollable")
            SCROLLABLE_TAB = (
                AppiumBy.XPATH,
                '//android.widget.TextView[@resource-id="android:id/title" and @text="TAB 2"]',
            )
