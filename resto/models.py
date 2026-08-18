from django.conf import settings
from django.db import models
from django.utils import timezone
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="menu_items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"

class Address(models.Model):
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}, {self.street}, {self.city}"

class Order(models.Model):
    STATUS_CART = "CART"
    STATUS_PENDING = "PENDING"       # checked out, awaiting confirmation
    STATUS_CONFIRMED = "CONFIRMED"   # restaurant accepted
    STATUS_PREPARING = "PREPARING"
    STATUS_ON_THE_WAY = "ON_THE_WAY"
    STATUS_DELIVERED = "DELIVERED"
    STATUS_CANCELED = "CANCELED"

    STATUS_CHOICES = [
        (STATUS_CART, "Cart"),
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_PREPARING, "Preparing"),
        (STATUS_ON_THE_WAY, "On the way"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELED, "Canceled"),
    ]

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="orders", on_delete=models.PROTECT)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CART)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.user} - {self.status}"

    def subtotal(self):
        return sum((item.price * item.quantity) for item in self.items.all())

    def total(self, delivery_fee=Decimal("3.00")):
        return (self.subtotal() + Decimal(delivery_fee))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name="+", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # snapshot of item price
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

    def line_total(self):
        return self.price * self.quantity