import pytest
from pages.inventory_page import InventoryPage



class TestCart:

    @pytest.mark.parametrize("products", [
        (["Sauce Labs Backpack", "Sauce Labs Bike Light"]),
        (["Sauce Labs Bolt T-Shirt"]),
    ])
    def test_add_to_cart(self, logged_in_user, products):
        """Dodaję produkty do koszyka."""
        inventory_page = InventoryPage(logged_in_user)

        # Dodawanie produktów
        for product in products:
            inventory_page.add_to_cart(product)

        inventory_products = inventory_page.get_added_products()

        # Przejście do koszyka
        cart_page = inventory_page.go_to_cart_page()
        cart_products = cart_page.get_products_from_cart()

        assert inventory_products == cart_products, (
            f"Mismatch between Inventory and Cart:\n"
            f"Inventory: {inventory_products}\nCart: {cart_products}"
        )

    @pytest.mark.parametrize("product", ["Sauce Labs Backpack"])
    def test_remove_product_from_cart(self, logged_in_user, product):
        """Usuwam produkt z koszyka."""
        inventory_page = InventoryPage(logged_in_user)
        inventory_page.add_to_cart(product)

        cart_page = inventory_page.go_to_cart_page()
        cart_page.remove_product_from_cart(product)
        cart_page.check_product_removed(product)

    @pytest.mark.parametrize("product", ["Sauce Labs Backpack"])
    def test_remove_product_from_inventory(self, logged_in_user, product):
        """Usuwam produkt z inventory i sprawdzam stan w koszyku."""
        inventory_page = InventoryPage(logged_in_user)
        inventory_page.add_to_cart(product)

        # Usunięcie bezpośrednio w Inventory
        inventory_page.remove_from_inventory(product)

        # Sprawdzenie w CartPage, że produkt faktycznie zniknął
        cart_page = inventory_page.go_to_cart_page()
        cart_page.check_product_removed(product)


