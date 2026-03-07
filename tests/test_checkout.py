from pages.inventory_page import InventoryPage


class TestCheckout:

    def test_checkout_overview(self, logged_in_user):
        # ---------------------- Step 1: Adds products to the cart ----------------------
        inventory_page = InventoryPage(logged_in_user)
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.add_to_cart("Sauce Labs Bike Light")

        # Downloading products added to your cart on the Inventory page
        inventory_products = inventory_page.get_added_products()

        # ---------------------- Step 2: Goes to the cart page ----------------------
        cart_page = inventory_page.go_to_cart_page()
        cart_products = cart_page.get_products_from_cart()

        # Checking that the products in the cart match the products added from Inventory
        assert inventory_products == cart_products, "Products or prices do not match between Inventory and Cart"

        # ---------------------- Step 3: Goes to Checkout ----------------------
        checkout_page = cart_page.go_to_checkout_page()

        # Filling out the delivery details
        checkout_page.input_delivery_data()

        # ---------------------- Step 4: Verifies products and totals in the overview ----------------------
        checkout_page.checkout_overview(cart_products)

        # ---------------------- Step 5: Finalizes and verifies orders ----------------------
        assert checkout_page.checkout_complete(), "Checkout was not completed successfully"
