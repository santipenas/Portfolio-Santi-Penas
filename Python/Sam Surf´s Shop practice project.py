import unittest
from datetime import datetime, timedelta

class TooManySurfboardsError(Exception):
    """Raised when trying to add too many surfboards to the cart."""
    pass

class CheckoutDateError(Exception):
    """Raised when the checkout date is in the past."""
    pass

class ShoppingCart:
    def __init__(self):
        self.surfboards = 0
        self.locals_discount = False
        self.checkout_date = None

    def add_surfboards(self, quantity):
        if quantity > 4:
            raise TooManySurfboardsError("Cannot add more than 4 surfboards at a time!")
        self.surfboards += quantity
        return f"Successfully added {quantity} surfboard{'s' if quantity > 1 else ''} to cart!"

    def apply_locals_discount(self):
        self.locals_discount = True

    def set_checkout_date(self, date):
        if date < datetime.now():
            raise CheckoutDateError("Checkout date cannot be in the past!")
        self.checkout_date = date

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_surfboard(self):
        result = self.cart.add_surfboards(1)
        self.assertEqual(result, 'Successfully added 1 surfboard to cart!')

    def test_add_multiple_surfboards(self):
        result = self.cart.add_surfboards(2)
        self.assertEqual(result, 'Successfully added 2 surfboards to cart!')

    def test_add_too_many_surfboards(self):
        with self.assertRaises(TooManySurfboardsError):
            self.cart.add_surfboards(5)

    @unittest.expectedFailure
    def test_apply_locals_discount(self):
        self.cart.apply_locals_discount()
        self.assertTrue(self.cart.locals_discount)

    @unittest.skip("Skipping test due to off-season policy changes.")
    def test_skip_too_many_surfboards(self):
        with self.assertRaises(TooManySurfboardsError):
            self.cart.add_surfboards(5)

    def test_add_surfboards_parameterized(self):
        for quantity in [2, 3, 4]:
            with self.subTest(quantity=quantity):
                result = self.cart.add_surfboards(quantity)
                self.assertEqual(result, f"Successfully added {quantity} surfboards to cart!")

    def test_set_checkout_date(self):
        future_date = datetime.now() + timedelta(days=1)
        self.cart.set_checkout_date(future_date)
        self.assertEqual(self.cart.checkout_date, future_date)

        with self.assertRaises(CheckoutDateError):
            self.cart.set_checkout_date(datetime.now() - timedelta(days=1))

if __name__ == "__main__":
    unittest.main()
