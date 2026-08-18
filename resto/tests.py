from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Restaurant, MenuItem, Order, OrderItem

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.rest = Restaurant.objects.create(name="Tasty", address="123 Main")
        self.item = MenuItem.objects.create(restaurant=self.rest, name="Burger", price="5.00", is_available=True)

    def test_cart_and_totals(self):
        order = Order.objects.create(user=self.user, restaurant=self.rest)
        OrderItem.objects.create(order=order, menu_item=self.item, quantity=2, price=self.item.price)
        self.assertEqual(order.subtotal(), self.item.price * 2)
        total = order.total()
        self.assertTrue(total >= order.subtotal())