from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem, Address
from django.contrib.auth import get_user_model

User = get_user_model()

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("id", "restaurant", "name", "description", "price", "is_available")

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ("id", "name", "description", "address", "phone", "menu_items")

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source="menu_item", read_only=True)
    class Meta:
        model = OrderItem
        fields = ("id", "menu_item", "menu_item_detail", "quantity", "price")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id", "user", "restaurant", "status", "address", "note", "items", "created_at", "updated_at")