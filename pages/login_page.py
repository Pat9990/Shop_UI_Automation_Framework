# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

from core.config import LOGIN_URL
from pages.base_page import BasePage



class LoginPage(BasePage):
    """Login page."""

    __username_field = (By.ID, "user-name")
    __password_field = (By.ID, "password")
    __login_btn = (By.ID, "login-button")
    __error_msg = (By.XPATH, "//div[@class='error-message-container error']")

    def __init__(self, driver: WebDriver):
        """Initializes the login page with the given WebDriver."""
        super().__init__(driver)

    def open_login_page(self):
        """Opens the login page."""
        self._open_url(LOGIN_URL)

    def login(self, username: str, password: str):
        """Logs in the user with the provided login and password."""
        self._type(self.__username_field, username)
        self._type(self.__password_field,password)
        self._click(self.__login_btn)

    def get_error_msg(self) -> str:
        """Returns the text of the login error message."""
        return self._get_text(self.__error_msg)



