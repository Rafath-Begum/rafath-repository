
# Create your views here.
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger('shop')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        logger.info(f"login done by : {username}")
        logger.debug(f"Login attempt for user: {username}")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            logger.info(f"User logged in: {username}")
            return redirect('home')
        else:
            logger.warning(f"Failed login for user: {username}")
    return render(request, 'shop/login.html')

def logout_view(request):
    logger.info(f"User logged out: {request.user.username}")
    logout(request)
    return redirect('login')

@login_required
def home(request):
    logger.debug(f"User {request.user.username} accessed home.")
    return render(request, 'shop/home.html')

