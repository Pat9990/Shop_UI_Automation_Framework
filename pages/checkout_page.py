from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout page – data entry, order summary, finalization."""

    __first_name_input = (By.ID, "first-name")
    __last_name_input = (By.ID, "last-name")
    __postal_code_input = (By.ID, "postal-code")
    __continue_btn = (By.ID, "continue")
    __item_total_field = (By.CLASS_NAME,"summary_subtotal_label")
    __finish_btn = (By.ID, "finish")
    __complete_header = (By.CLASS_NAME,"complete-header")

    def __init__(self, driver:WebDriver):
        super().__init__(driver)

    # ---------------------- User data ----------------------
    def input_delivery_data(self, first_name:str = "Anna", last_name:str = "Nowak", postal_code:int = 2365):
        """Fills out the delivery details and clicks Continue."""
        self._type(self.__first_name_input,first_name)
        self._type(self.__last_name_input,last_name)
        self._type(self.__postal_code_input,postal_code)
        self._click(self.__continue_btn)

    # ---------------------- Products and prices ----------------------
    def get_products_from_overview(self) -> dict[str,str]:
         """Returns a dictionary of products added to the cart: {product_name: price}."""
         return self._get_products()

    def get_total_price_displayed(self) -> float:
        """Gets the value for products from the Checkout page. Then returns the total."""
        price = self._get_text(self.__item_total_field)
        price_number = float(price.lstrip("Item total: $"))
        return price_number

    def check_items_price(self, prices:list):
        """Checks if the calculated total is the same as the one displayed on the Checkout page."""
        total_price_calculated = sum(self._get_number_of_prices(prices))
        total_price_displayed = self.get_total_price_displayed()
        assert total_price_calculated == total_price_displayed, "Total items price is incorrect"

    # ---------------------- Checkout ----------------------
    def checkout_overview(self, products_cart_dict: dict[str,str]):
        """Verifies the products in the overview and their price sum. Does not complete checkout – separate finish_order() method for finalization."""
        products_overview_dict = self.get_products_from_overview()
        assert products_overview_dict == products_cart_dict, "Incorrect products in overview"
        prices_list = list(products_cart_dict.values())
        self.check_items_price(prices_list)
        self._click(self.__finish_btn)

    def checkout_complete(self) -> bool:
        """Checks whether checkout has been completed. Returns True if the order confirmation text is visible."""
        try:
            self.wait_until_text_is_visible(self.__complete_header, "Thank you for your order!")
            return True
        except TimeoutException:
            return False






