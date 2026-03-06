import pytest

from pages.login_page import LoginPage
from core.config import INVENTORY_URL, ERR_INCORRECT, ERR_EMPTY_USERNAME, ERR_EMPTY_PASSWORD, STANDARD_USER, \
    STANDARD_PASSWORD


class TestLoginPage:

    def test_positive_login(self, driver):
        """Testuje logowanie poprawnymi danymi"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login(STANDARD_USER,STANDARD_PASSWORD)

        assert login_page.current_url == INVENTORY_URL, "Login failed: You are not logged in"

    @pytest.mark.parametrize(
        "username,password",
        [
            ("incorrect_username", "secret_sauce"),
            ("standard_user", "incorrect_password"),
        ]
    )
    def test_negative_incorrect_data(self, driver, username, password):
        """Testuje logowanie niepoprawnymi danymi"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login(username, password)

        assert login_page.get_error_msg() == ERR_INCORRECT, "Incorrect error message for invalid credentials"

    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("", "secret_sauce", ERR_EMPTY_USERNAME),
            ("standard_user", "", ERR_EMPTY_PASSWORD),
        ]
    )
    def test_negative_empty_data(self, driver, username, password, expected_error):
        """Testuje logowanie niekompletnymi danymi"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login(username, password)

        assert login_page.get_error_msg() == expected_error, "Incorrect error message for empty fields"