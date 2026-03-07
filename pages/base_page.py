from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage():
    """
    The base class for all pages in the application.
    Contains basic methods for finding elements, clicking,
    entering text, waiting, and retrieving information from the page.
    """

    def __init__(self, driver: WebDriver):
        """Initialization with browser."""
        self._driver = driver

    # ---------------------- Finding elements ----------------------
    def _find(self, locator: tuple[str,str]) -> WebElement:
        """Returns a single visible item."""
        self._wait_until_element_is_visible(locator)
        return self._driver.find_element(*locator)

    def _find_all(self, locator: tuple[str,str]) -> list[WebElement]:
        """Returns all visible elements matching the locator."""
        wait = WebDriverWait(self._driver, 10)
        return wait.until(EC.visibility_of_all_elements_located(locator))

    # ---------------------- Interactions ----------------------
    def _type(self, locator: tuple[str,str], text: str):
        """Inputs text into the field indicated by the locator."""
        self._find(locator).send_keys(text)

    def _click(self, locator: tuple[str,str]):
        """Clicks into element"""
        self._find(locator).click()

    def _get_text(self, locator: tuple[str,str]) -> str:
        """Returns the text of the item."""
        return self._find(locator).text

    # ---------------------- Waits ----------------------
    def _wait_until_element_is_visible(self, locator: tuple[str,str], time:int = 10):
        """Waits until the element becomes visible."""
        wait = WebDriverWait(self._driver, time)
        wait.until(EC.visibility_of_element_located(locator))

    def _wait_until_element_is_not_visible(self, locator: tuple[str,str], time:int = 10) -> bool:
        """Waits for the element to disappear. Returns True if invisible."""
        wait = WebDriverWait(self._driver, time)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_until_text_is_visible(self, locator:tuple[str,str], expected_text:str, time:int = 10):
        """Waits for text to appear in the element."""
        wait = WebDriverWait(self._driver, time)
        wait.until(EC.text_to_be_present_in_element(locator, expected_text))

    # ---------------------- Navigation ----------------------
    def _open_url(self, url: str):
        """Opens the given URL."""
        self._driver.get(url)

    @property
    def current_url(self) -> str:
        """Returns the current page URL."""
        return self._driver.current_url

    # ---------------------- Additional methods ----------------------
    def _get_products(self) -> dict[str, str]:
        """Returns a dictionary of products {name: price} on the page."""
        products = {}
        names = self._find_all((By.CLASS_NAME, "inventory_item_name"))
        prices = self._find_all((By.CLASS_NAME, "inventory_item_price"))

        for name, price in zip(names, prices):
            products[name.text] = price.text

        return products

    def _get_number_of_prices(self, prices:list[str]) -> list[float]:
        """Converts a list of prices from text to float."""
        prices_numbers =[float(price.lstrip("$")) for price in prices]
        return prices_numbers