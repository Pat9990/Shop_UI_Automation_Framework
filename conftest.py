import pytest
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from core import config


# --------------------- Driver fixture ---------------------
@pytest.fixture
def driver():
    """Tworzy instancję przeglądarki Firefox i zamyka ją po teście."""
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

# --------------------- Logged in user fixture ---------------------
@pytest.fixture
def logged_in_user(driver):
    """Loguje użytkownika standardowego do aplikacji."""
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(config.STANDARD_USER, config.STANDARD_PASSWORD)
    return driver

# --------------------- Raporty HTML ---------------------
def pytest_configure(config):
    """Automatyczna konfiguracja raportów HTML."""
    reports_folder = "reports"
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = os.path.join(reports_folder, f"report_{now}.html")
    config.option.self_contained_html = True