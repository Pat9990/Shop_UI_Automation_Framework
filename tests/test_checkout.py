from pages.inventory_page import InventoryPage


class TestCheckout:

    def test_checkout_overview(self, logged_in_user):
        # ---------------------- Krok 1: Dodanie produktów do koszyka ----------------------
        inventory_page = InventoryPage(logged_in_user)
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.add_to_cart("Sauce Labs Bike Light")

        # Pobranie produktów dodanych do koszyka na stronie Inventory
        inventory_products = inventory_page.get_added_products()

        # ---------------------- Krok 2: Przejście do strony koszyka ----------------------
        cart_page = inventory_page.go_to_cart_page()
        cart_products = cart_page.get_products_from_cart()

        # Sprawdzenie, że produkty w koszyku odpowiadają produktom dodanym z Inventory
        assert inventory_products == cart_products, "Products or prices do not match between Inventory and Cart"

        # ---------------------- Krok 3: Przejście do Checkout ----------------------
        checkout_page = cart_page.go_to_checkout_page()

        # Wypełnienie danych dostawy
        checkout_page.input_delivery_data()

        # ---------------------- Krok 4: Weryfikacja produktów i sumy w overview ----------------------
        checkout_page.checkout_overview(cart_products)

        # ---------------------- Krok 5: Finalizacja i weryfikacja zamówienia ----------------------
        assert checkout_page.checkout_complete(), "Checkout was not completed successfully"
