from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage



class InventoryPage(BasePage):
    """Strona Inventory – dodawanie, usuwanie produktów, sortowanie i pobieranie info."""

    __product_names = (By.CLASS_NAME, "inventory_item_name")
    __sort_dropdown = (By.CLASS_NAME, "product_sort_container")
    __cart_btn = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    # ---------------------- Prywatne lokatory dynamiczne ----------------------
    def _add_btn_locator(self, product_name: str):
        return (By.XPATH,
                f".//div[contains(text(),'{product_name}')]/ancestor::div[@class='inventory_item']//button[contains(@id,'add-to-cart')]")

    def _remove_btn_locator(self, product_name: str):
        return (By.XPATH,
                f".//div[contains(text(),'{product_name}')]/ancestor::div[@class='inventory_item']//button[contains(@id,'remove')]")

    def _product_price_locator(self, product_name: str):
        return (By.XPATH,
                f".//div[contains(text(),'{product_name}')]/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']")

    # ---------------- Produkty i ceny -----------------------------
    def get_product_names(self) -> list[str]:
        """Zwraca listę nazw wszystkich produktów na stronie Inventory."""
        products = self._get_products()
        return list(products.keys())

    def get_product_prices(self) -> list[float]:
        """Zwraca listę cen wszystkich produktów na stronie Inventory."""
        products = self._get_products()
        prices = products.values()
        return list(self._get_number_of_prices(prices))

    def get_added_products(self) -> dict[str,str]:
        """Zwraca słownik produktów dodanych do koszyka: {nazwa_produktu: cena}, które mają przycisk 'Remove' (czyli są w koszyku)."""
        product_in_cart_locator = (By.XPATH,"//button[contains(text(),'Remove')]/ancestor::div[@class='inventory_item']//div[@class= 'inventory_item_name ']")
        products = {}
        products_elements = self._find_all(product_in_cart_locator)
        assert products_elements, "No products found in inventory cart"

        for el in products_elements:
            name = el.text
            price = self._get_text(self._product_price_locator(name))
            products[name] = price
        return products

    # ---------------------- Dodawanie / usuwanie ----------------------
    def add_to_cart(self, product_name: str):
        """Kliknięcie przycisku 'Add to cart' dla podanego produktu."""
        self._click(self._add_btn_locator(product_name))

    def remove_from_inventory(self, product_name: str):
        """Kliknięcie 'Remove' dla produktu i oczekiwanie na pojawienie się przycisku 'Add to cart'."""
        self._click(self._remove_btn_locator(product_name))
        self._wait_until_element_is_visible(self._add_btn_locator(product_name))

    # ---------------------- Sortowanie ----------------------
    def select_sort_option(self, option:str):
        """Wybór opcji sortowania w dropdownie."""
        select_element = self._find(self.__sort_dropdown)
        select = Select(select_element)
        select.select_by_visible_text(option)

    def sort_az(self):
        """Sortowanie A-Z"""
        self.select_sort_option("Name (A to Z)")

    def sort_za(self):
        """Sortowanie Z-A"""
        self.select_sort_option("Name (Z to A)")

    def sort_price_low_high(self):
        """Sortowanie od najniższej ceny"""
        self.select_sort_option("Price (low to high)")

    def sort_price_high_low(self):
        """Sortowanie od najwyższej ceny"""
        self.select_sort_option("Price (high to low)")

    def check_sorting_by_name(self, reverse):
        """Sprawdza, czy produkty są posortowane alfabetycznie (A-Z / Z-A)."""
        ui_products_names = self.get_product_names()
        expected_products_names = sorted(ui_products_names, reverse=reverse)
        assert ui_products_names == expected_products_names, f"Products are not sorted correctly"

    def check_sorting_by_price(self, reverse):
        """Sprawdza, czy produkty są posortowane według ceny (low-high / high-low)."""
        ui_products_prices = self.get_product_prices()
        expected_products_prices = sorted(ui_products_prices, reverse=reverse)
        assert ui_products_prices == expected_products_prices, f"Products are not sorted correctly"

    # ---------------------- Nawigacja ----------------------
    def go_to_cart_page(self):
        """Przechodzi do strony koszyka. Import wewnętrzny zapobiega circular import."""
        from pages.cart_page import CartPage
        self._click(self.__cart_btn)
        return CartPage(self._driver)




