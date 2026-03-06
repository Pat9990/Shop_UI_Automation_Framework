import pytest

from pages.inventory_page import InventoryPage


class TestInventory:

    @pytest.mark.parametrize(
        "sort_method, reverse",
        [
            ("sort_az", False),
            ("sort_za", True)
        ]
    )
    def test_sort_by_name(self, logged_in_user, sort_method, reverse):
        """Testuje sortowanie produktów po nazwie"""
        inventory_page = InventoryPage(logged_in_user)
        getattr(inventory_page, sort_method)()
        inventory_page.check_sorting_by_name(reverse)

    @pytest.mark.parametrize(
        "sort_method, reverse",
        [
            ("sort_price_low_high", False),
            ("sort_price_high_low", True)
        ]
    )
    def test_sort_by_price(self, logged_in_user, sort_method, reverse):
        """Testuje sortowanie produktów po cenie"""
        inventory_page = InventoryPage(logged_in_user)
        getattr(inventory_page, sort_method)()
        inventory_page.check_sorting_by_price(reverse)
