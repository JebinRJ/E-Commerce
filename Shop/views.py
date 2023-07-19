from django.shortcuts import render, redirect
from Shop.models import *
from django.http import JsonResponse
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_quantity = data['product_quantity']
            product_id = data['pid']
            # print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id, product_quantity=product_quantity):
                    return JsonResponse({'status': 'Product already in cart'}, status=200)
                else:
                    if product_status.quantity >= product_quantity:
                        Cart.objects.create(
                            user=request.user, product_id=product_id, product_quantity=product_quantity)
                        return JsonResponse({'status': 'Product added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product not available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully!")
            return redirect("login")
    return render(request, 'shop/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect("/")

        else:
            messages.error(request, "Username and Password does not exist")
            return redirect("/login")

    return render(request, 'shop/login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Succssfully")
    return redirect("/login")


def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, 'shop/collections.html', {'category': category})


def collectionsview(request, name):
    if (Category.objects.filter(status=0, name=name)):
        products = Product.objects.filter(category__name=name)
        return render(request, 'shop/products/index.html', {'products': products, 'category_name': name})
    else:
        messages.warning(request, "Not Found")
        return redirect('collections')


def product_details(request, cname, pname):
    if (Category.objects.filter(status=0, name=cname)):
        if (Product.objects.filter(status=0, name=pname)):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products})
        else:
            messages.error(request, "No Such file found")
            return redirect("collections")
    else:
        messages.error(request, "Not Found")
        return redirect("collections")


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    else:
        return redirect("/")


def fav(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Fav.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product already in Favourite'}, status=200)
                else:
                    Fav.objects.create(user=request.user,
                                       product_id=product_id)
                    return JsonResponse({'status': 'Product Added'}, status=200)
        else:
            return JsonResponse({'status': 'Login to add Favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Fav.objects.filter(user=request.user)
        return render(request, "shop/Fav.html", {"fav": fav})
    else:
        return redirect("/")


def remove_fav(request, fid):
    cartitem = Fav.objects.get(id=fid)
    cartitem.delete()
    return redirect("favviewpage")


def remove_cart(request, cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("cart")


# Create your views here.
