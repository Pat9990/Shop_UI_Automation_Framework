from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Strona Checkout – wprowadzanie danych, podsumowanie zamówienia, finalizacja."""

    __first_name_input = (By.ID, "first-name")
    __last_name_input = (By.ID, "last-name")
    __postal_code_input = (By.ID, "postal-code")
    __continue_btn = (By.ID, "continue")
    __item_total_field = (By.CLASS_NAME,"summary_subtotal_label")
    __finish_btn = (By.ID, "finish")
    __complete_header = (By.CLASS_NAME,"complete-header")

    def __init__(self, driver:WebDriver):
        super().__init__(driver)

    # ---------------------- Dane użytkownika ----------------------
    def input_delivery_data(self, first_name:str = "Anna", last_name:str = "Nowak", postal_code:int = 2365):
        """Wypełnia dane dostawy i klika Continue."""
        self._type(self.__first_name_input,first_name)
        self._type(self.__last_name_input,last_name)
        self._type(self.__postal_code_input,postal_code)
        self._click(self.__continue_btn)

    # ---------------------- Produkty i ceny ----------------------
    def get_products_from_overview(self) -> dict[str,str]:
         """Zwraca słownik produktów dodanych do koszyka: {nazwa_produktu: cena}"""
         return self._get_products()

    def get_total_price_displayed(self) -> float:
        """Pobiera wartość za produkty ze strony Checkout. Następnie zwraca wartość sumy."""
        price = self._get_text(self.__item_total_field)
        price_number = float(price.lstrip("Item total: $"))
        return price_number

    def check_items_price(self, prices:list):
        """Sprawdza, czy suma obliczona jest taka sama jak wyświetlana na Checkout stronie"""
        total_price_calculated = sum(self._get_number_of_prices(prices))
        total_price_displayed = self.get_total_price_displayed()
        assert total_price_calculated == total_price_displayed, "Total items price is incorrect"

    # ---------------------- Checkout ----------------------
    def checkout_overview(self, products_cart_dict: dict[str,str]):
        """Weryfikuje produkty w overview i ich sumę cen.Nie kończy checkoutu – osobna metoda finish_order() do finalizacji."""
        products_overview_dict = self.get_products_from_overview()
        assert products_overview_dict == products_cart_dict, "Incorrect products in overview"
        prices_list = list(products_cart_dict.values())
        self.check_items_price(prices_list)
        self._click(self.__finish_btn)

    def checkout_complete(self) -> bool:
        """Sprawdza, czy checkout został zakończony.Zwraca True, jeśli widoczny jest tekst potwierdzający zamówienie."""
        try:
            self.wait_until_text_is_visible(self.__complete_header, "Thank you for your order!")
            return True
        except TimeoutException:
            return False






