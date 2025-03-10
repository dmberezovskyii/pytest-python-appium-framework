import pytest
from screens.main_screen.main_screen import MainScreen


class TestClick:
    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
        """Setup common objects for tests after address is set."""
        self.main_screen = MainScreen(driver)
        
    def test_click(self, setup):
        self.main_screen.click_on_text_link()
    
    def test_tap(self, setup):
        self.main_screen.tap_on_text_link()