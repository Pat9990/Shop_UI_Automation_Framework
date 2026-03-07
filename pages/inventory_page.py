from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Inventory page – adding, removing products, sorting and downloading information."""

    __product_names = (By.CLASS_NAME, "inventory_item_name")
    __sort_dropdown = (By.CLASS_NAME, "product_sort_container")
    __cart_btn = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    # ---------------------- Private dynamic locators ----------------------
    def _add_btn_locator(self, product_name: str):
        return (By.XPATH,
                f".//div[contains(text(),'{product_name}')]/ancestor::div[@class='inventory_item']//button[contains(@id,'add-to-cart')]")

    def _remove_btn_locator(self, product_name: str):
        return (By.XPATH,
                f".//div[contains(text(),'{product_name}')]/ancestor::div[@class='inventory_item']//button[contains(@id,'remove')]")

    def _product_price_locator(self, product_name: str):
        return (By.XPATH,
                f".//div[contains(text(),'{product_name}')]/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']")

    # ---------------- Products and prices -----------------------------
    def get_product_names(self) -> list[str]:
        """Returns a list of the names of all products on the Inventory page."""
        products = self._get_products()
        return list(products.keys())

    def get_product_prices(self) -> list[float]:
        """Returns a list of prices for all products on the Inventory page."""
        products = self._get_products()
        prices = products.values()
        return list(self._get_number_of_prices(prices))

    def get_added_products(self) -> dict[str,str]:
        """Returns a dictionary of products added to the cart: {product_name: price} that have a 'Remove' button (i.e. are in the cart)."""
        product_in_cart_locator = (By.XPATH,"//button[contains(text(),'Remove')]/ancestor::div[@class='inventory_item']//div[@class= 'inventory_item_name ']")
        products = {}
        products_elements = self._find_all(product_in_cart_locator)
        assert products_elements, "No products found in inventory cart"

        for el in products_elements:
            name = el.text
            price = self._get_text(self._product_price_locator(name))
            products[name] = price
        return products

    # ---------------------- Adding/Removing ----------------------
    def add_to_cart(self, product_name: str):
        """Clicking the 'Add to cart' button for the given product."""
        self._click(self._add_btn_locator(product_name))

    def remove_from_inventory(self, product_name: str):
        """Clicking 'Remove' for a product and waiting for the 'Add to cart' button to appear."""
        self._click(self._remove_btn_locator(product_name))
        self._wait_until_element_is_visible(self._add_btn_locator(product_name))

    # ---------------------- Sorting ----------------------
    def select_sort_option(self, option:str):
        """Selecting sorting options in the dropdown."""
        select_element = self._find(self.__sort_dropdown)
        select = Select(select_element)
        select.select_by_visible_text(option)

    def sort_az(self):
        """A-Z sorting"""
        self.select_sort_option("Name (A to Z)")

    def sort_za(self):
        """Z-A sorting"""
        self.select_sort_option("Name (Z to A)")

    def sort_price_low_high(self):
        """Sorting by lowest price"""
        self.select_sort_option("Price (low to high)")

    def sort_price_high_low(self):
        """Sorting by highest price"""
        self.select_sort_option("Price (high to low)")

    def check_sorting_by_name(self, reverse):
        """Checks if products are sorted alphabetically (A-Z / Z-A)."""
        ui_products_names = self.get_product_names()
        expected_products_names = sorted(ui_products_names, reverse=reverse)
        assert ui_products_names == expected_products_names, f"Products are not sorted correctly"

    def check_sorting_by_price(self, reverse):
        """Checks if products are sorted by price (low-high / high-low)."""
        ui_products_prices = self.get_product_prices()
        expected_products_prices = sorted(ui_products_prices, reverse=reverse)
        assert ui_products_prices == expected_products_prices, f"Products are not sorted correctly"

    # ---------------------- Navigation ----------------------
    def go_to_cart_page(self):
        """Goes to the cart page. Internal import prevents circular import."""
        from pages.cart_page import CartPage
        self._click(self.__cart_btn)
        return CartPage(self._driver)




