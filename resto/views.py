from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import Restaurant, MenuItem, Order, OrderItem, Address
from .forms import AddToCartForm, CheckoutForm
from decimal import Decimal
from django.db import transaction

class RestaurantListView(ListView):
    model = Restaurant
    template_name = "delivery/restaurant_list.html"
    context_object_name = "restaurants"

class MenuDetailView(DetailView):
    model = Restaurant
    template_name = "delivery/menu_detail.html"
    context_object_name = "restaurant"

@method_decorator(login_required, name="dispatch")
class AddToCartView(View):
    def post(self, request, restaurant_id, item_id):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        item = get_object_or_404(MenuItem, pk=item_id, restaurant=restaurant, is_available=True)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data["quantity"]
            # Use or create cart order
            order, created = Order.objects.get_or_create(user=request.user, restaurant=restaurant, status=Order.STATUS_CART)
            order_item, created_item = OrderItem.objects.get_or_create(order=order, menu_item=item, defaults={"quantity": qty, "price": item.price})
            if not created_item:
                order_item.quantity += qty
                order_item.save()
        return redirect("delivery:cart")

@method_decorator(login_required, name="dispatch")
class CartView(View):
    def get(self, request):
        # show carts across restaurants: pick the last cart if multiple exist, or show all carts - we'll show last cart
        cart = Order.objects.filter(user=request.user, status=Order.STATUS_CART).order_by("-created_at").first()
        return render(request, "delivery/cart.html", {"cart": cart})

@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    def get(self, request):
        cart = Order.objects.filter(user=request.user, status=Order.STATUS_CART).order_by("-created_at").first()
        if not cart:
            return redirect("delivery:restaurant_list")
        form = CheckoutForm(user=request.user)
        return render(request, "delivery/checkout.html", {"cart": cart, "form": form})

    @transaction.atomic
    def post(self, request):
        cart = Order.objects.filter(user=request.user, status=Order.STATUS_CART).order_by("-created_at").first()
        if not cart:
            return redirect("delivery:restaurant_list")
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            address = form.cleaned_data.get("address")
            if not address:
                address = Address.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data.get("full_name"),
                    street=form.cleaned_data.get("street"),
                    city=form.cleaned_data.get("city"),
                    zipcode=form.cleaned_data.get("zipcode"),
                    phone=form.cleaned_data.get("phone"),
                )
            cart.address = address
            cart.note = form.cleaned_data.get("note")
            cart.status = Order.STATUS_PENDING
            cart.save()
            # normally trigger notification to restaurant or payment process here
            return redirect("delivery:order_detail", pk=cart.pk)
        return render(request, "delivery/checkout.html", {"cart": cart, "form": form})

@method_decorator(login_required, name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "delivery/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)