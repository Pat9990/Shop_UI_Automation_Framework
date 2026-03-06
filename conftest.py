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

# --------------------- HTML Report Configuration ---------------------
def pytest_configure(config):
    """Automatically configure HTML reports."""
    reports_folder = "reports"
    screenshots_folder = os.path.join(reports_folder, "screenshots")

    os.makedirs(reports_folder, exist_ok=True)
    os.makedirs(screenshots_folder, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = os.path.join(reports_folder, f"report_{now}.html")
    config.option.self_contained_html = True


# --------------------- Screenshot on failure ---------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to report if test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")

        if driver:
            screenshots_folder = "reports/screenshots"
            os.makedirs(screenshots_folder, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(
                screenshots_folder,
                f"{item.name}_{timestamp}.png"
            )

            driver.save_screenshot(screenshot_path)