from contextlib import redirect_stdout
from http.client import HTTPResponse
from django.shortcuts import render
from store.models import Product
from .models import Cart, CartItem
# Create your views here.
from django.http import HttpResponse
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart id present in the session
    except Cart.DoesNotExist:
        cart =Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart = cart)
        cart_item.quantity += 1 # cart item quantity increse
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product, 
            quantity =1,
            cart = cart
        )
        cart_item.save()
    return HttpResponse(cart_item.product)
    exit()
def cart(request):
    return render(request, 'store/cart.html')