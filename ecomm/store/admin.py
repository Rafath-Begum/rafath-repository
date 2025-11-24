# Register your models here.
from django.contrib import admin
from .models import Product

admin.site.register(Product)
from .models import Category, Productl, Customer, Order

admin.site.register(Category)
admin.site.register(Productl)
admin.site.register(Customer)
admin.site.register(Order)