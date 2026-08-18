from django.contrib import admin
from .models import Restaurant, MenuItem, Address, Order, OrderItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "address")
    search_fields = ("name",)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "is_available")
    list_filter = ("restaurant", "is_available")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "city", "is_default")
    list_filter = ("city", "is_default")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("menu_item", "price", "quantity")
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "status", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "updated_at")
