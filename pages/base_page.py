from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage():
    """Bazowa klasa dla wszystkich stron w aplikacji.
        Zawiera podstawowe metody do znajdowania elementów, kliknięć,
        wpisywania tekstu, oczekiwań i pobierania informacji ze strony.
        """

    def __init__(self, driver: WebDriver):
        """Inicjalizacja z przeglądarką."""
        self._driver = driver

    # ---------------------- Znajdowanie elementów ----------------------
    def _find(self, locator: tuple[str,str]) -> WebElement:
        """Zwraca pojedynczy widoczny element."""
        self._wait_until_element_is_visible(locator)
        return self._driver.find_element(*locator)

    def _find_all(self, locator: tuple[str,str]) -> list[WebElement]:
        """Zwraca wszystkie widoczne elementy pasujące do lokatora."""
        wait = WebDriverWait(self._driver, 10)
        return wait.until(EC.visibility_of_all_elements_located(locator))

    # ---------------------- Interakcje ----------------------
    def _type(self, locator: tuple[str,str], text: str):
        """Wpisuje tekst w pole wskazane lokatorem."""
        self._find(locator).send_keys(text)

    def _click(self, locator: tuple[str,str]):
        """Kliknięcie elementu."""
        self._find(locator).click()

    def _get_text(self, locator: tuple[str,str]) -> str:
        """Zwraca tekst elementu."""
        return self._find(locator).text

    # ---------------------- Wait'y ----------------------
    def _wait_until_element_is_visible(self, locator: tuple[str,str], time:int = 10):
        """Czeka, aż element stanie się widoczny."""
        wait = WebDriverWait(self._driver, time)
        wait.until(EC.visibility_of_element_located(locator))

    def _wait_until_element_is_not_visible(self, locator: tuple[str,str], time:int = 10) -> bool:
        """Czeka, aż element zniknie. Zwraca True po niewidoczności."""
        wait = WebDriverWait(self._driver, time)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_until_text_is_visible(self, locator:tuple[str,str], expected_text:str, time:int = 10):
        """Czeka, aż tekst pojawi się w elemencie."""
        wait = WebDriverWait(self._driver, time)
        wait.until(EC.text_to_be_present_in_element(locator, expected_text))

    # ---------------------- Nawigacja ----------------------
    def _open_url(self, url: str):
        """Otwiera podany URL."""
        self._driver.get(url)

    @property
    def current_url(self) -> str:
        """Zwraca aktualny URL strony."""
        return self._driver.current_url

    # ---------------------- Pomocnicze metody ----------------------
    def _get_products(self) -> dict[str, str]:
        """Zwraca słownik produktów {nazwa: cena} na stronie."""
        products = {}
        names = self._find_all((By.CLASS_NAME, "inventory_item_name"))
        prices = self._find_all((By.CLASS_NAME, "inventory_item_price"))

        for name, price in zip(names, prices):
            products[name.text] = price.text

        return products

    def _get_number_of_prices(self, prices:list[str]) -> list[float]:
        """Konwertuje listę cen z tekstu na float."""
        prices_numbers =[float(price.lstrip("$")) for price in prices]
        return prices_numbers