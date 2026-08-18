from django.urls import path, include
from . import views
from rest_framework import routers
from . import api_views

app_name = "delivery"

urlpatterns = [
    path("", views.RestaurantListView.as_view(), name="restaurant_list"),
    path("restaurant/<int:pk>/", views.MenuDetailView.as_view(), name="menu_detail"),
    path("add-to-cart/<int:restaurant_id>/item/<int:item_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("order/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    # API routes
]
# API router
router = routers.DefaultRouter()
router.register(r"restaurants", api_views.RestaurantViewSet, basename="restaurant")
router.register(r"menu-items", api_views.MenuItemViewSet, basename="menuitem")
router.register(r"orders", api_views.OrderViewSet, basename="order")

urlpatterns += [
    path("api/", include((router.urls, "api"), namespace="api")),
]from django.urls import path, include
from . import views
from rest_framework import routers
from . import api_views

app_name = "delivery"

urlpatterns = [
    path("", views.RestaurantListView.as_view(), name="restaurant_list"),
    path("restaurant/<int:pk>/", views.MenuDetailView.as_view(), name="menu_detail"),
    path("add-to-cart/<int:restaurant_id>/item/<int:item_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("order/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    # API routes
]
# API router
router = routers.DefaultRouter()
router.register(r"restaurants", api_views.RestaurantViewSet, basename="restaurant")
router.register(r"menu-items", api_views.MenuItemViewSet, basename="menuitem")
router.register(r"orders", api_views.OrderViewSet, basename="order")

urlpatterns += [
    path("api/", include((router.urls, "api"), namespace="api")),
]