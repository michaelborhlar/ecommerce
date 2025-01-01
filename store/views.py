# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product, Order

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Incorrect username or password.')
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def checkout(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        quantity = int(request.POST['quantity'])
        if product.quantity >= quantity:
            total_price = product.price * quantity
            product.quantity -= quantity
            product.save()
            Order.objects.create(user=request.user, product=product, quantity=quantity, total_price=total_price)
            messages.success(request, 'Order placed successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Not enough stock.')
    return render(request, 'store/checkout.html', {'product': product})

