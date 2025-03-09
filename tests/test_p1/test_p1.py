from screens.main.main_screen import MainScreen


class TestClick:
    def test_click(self, driver):
        main = MainScreen(driver)
        main.click_on_text_link()
