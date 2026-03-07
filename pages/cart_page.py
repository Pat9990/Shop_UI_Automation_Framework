from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from pages.base_page import BasePage


class CartPage(BasePage):
    """Cart page – download products, remove, continue shopping and proceed to checkout."""

    __checkout_btn = (By.ID,"checkout")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    # ---------------------- Private dynamic locators ----------------------
    def _remove_btn_locator(self, product: str):
        """Returns the locator of the 'Remove' button for the given product."""
        return (By.XPATH,f".//div[contains(text(),'{product}')]/ancestor::div[@class='cart_item']//button[contains(text(),'Remove')]")

    def _product_locator(self, product: str):
        """Returns the locator of the product in the cart by name."""
        return (By.XPATH,f".//div[@class='inventory_item_name' and contains(text(),'{product}')]")

    # ---------------------- Products in the cart ----------------------
    def get_products_from_cart(self) -> dict[str,str]:
         """Returns a dictionary of products added to the cart: {product_name: price}"""
         return self._get_products()

    # ---------------------- Actions ----------------------
    def remove_product_from_cart(self,product:str):
        """Removes a given product from the cart."""
        self._click(self._remove_btn_locator(product))

    def check_product_removed(self,product:str):
        """
        Checks whether a product has been removed from the cart.
        It will throw an AssertionError exception if it is still visible.
        """
        assert self._wait_until_element_is_not_visible(self._product_locator(product)), f"Product '{product}' not removed from cart"

    def go_to_checkout_page(self):
        """Goes to the checkout page and returns a Checkout Page object."""
        from pages.checkout_page import CheckoutPage
        self._click(self.__checkout_btn)
        return CheckoutPage(self._driver)


