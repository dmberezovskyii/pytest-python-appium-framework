import pytest
from screens.main_screen.main_screen import MainScreen


class TestBaseActions:
    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
        """Setup common objects for tests after address is set."""
        self.main_screen = MainScreen(driver)

    def test_click(self, setup):
        self.main_screen.click_on_text_link()

    def test_tap(self, setup):
        self.main_screen.tap_on_text_link()

    def test_scroll_by_coordinates(self, setup):
        self.main_screen.scroll_view_by_coordinates(direction="down")
        self.main_screen.scroll("up")

    def test_sroll_to_element(self, setup):
        self.main_screen.scroll_to_image_button()

    def test_scroll_util_visible(self, setup):
        self.main_screen.scroll_until_text_field_visible()
