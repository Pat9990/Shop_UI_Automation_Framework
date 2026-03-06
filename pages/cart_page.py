from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from pages.base_page import BasePage


class CartPage(BasePage):
    """Strona koszyka – pobieranie produktów, usuwanie, kontynuowanie zakupów i przejście do checkout."""

    __checkout_btn = (By.ID,"checkout")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    # ---------------------- Prywatne lokatory dynamiczne ----------------------
    def _remove_btn_locator(self, product: str):
        """Zwraca locator przycisku 'Remove' dla podanego produktu."""
        return (By.XPATH,f".//div[contains(text(),'{product}')]/ancestor::div[@class='cart_item']//button[contains(text(),'Remove')]")

    def _product_locator(self, product: str):
        """Zwraca locator produktu w koszyku po nazwie."""
        return (By.XPATH,f".//div[@class='inventory_item_name' and contains(text(),'{product}')]")

    # ---------------------- Produkty w koszyku ----------------------
    def get_products_from_cart(self) -> dict[str,str]:
         """Zwraca słownik produktów dodanych do koszyka: {nazwa_produktu: cena}"""

         return self._get_products()

    # ---------------------- Akcje ----------------------
    def remove_product_from_cart(self,product:str):
        """Usuwa dany produkt z koszyka."""
        self._click(self._remove_btn_locator(product))

    def check_product_removed(self,product:str):
        """
        Sprawdza, czy produkt został usunięty z koszyka.
        Zgłosi wyjątek AssertionError, jeśli nadal jest widoczny.
        """
        assert self._wait_until_element_is_not_visible(self._product_locator(product)), f"Product '{product}' not removed from cart"

    def go_to_checkout_page(self):
        """Przechodzi do strony checkout i zwraca obiekt CheckoutPage."""
        from pages.checkout_page import CheckoutPage
        self._click(self.__checkout_btn)
        return CheckoutPage(self._driver)


