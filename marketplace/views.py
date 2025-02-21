from .models import Vendor, Product,Order,Cart
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

def vendor_list(request):
    vendors = Vendor.objects.all()  # Fetch all vendors
    return render(request, 'vendor_list.html', {'vendors': vendors})  # Pass data to template


def vendor_details(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)  # Fetch vendor by ID
    products = Product.objects.filter(vendor=vendor)  # Get products by vendor
    return render(request, 'vendor_details.html', {'vendor': vendor, 'products': products})


def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'product_list.html', {'products': products})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Fetch product by ID
    return render(request, 'product_details.html', {'product': product})



def cart_view(request):
    cart = request.session.get('cart', {})  # Get cart from session
    return render(request, 'cart.html', {'cart': cart})




def order_list(request):
    orders = Order.objects.filter(user=request.user)  # Fetch user orders
    return render(request, 'order_list.html', {'orders': orders})



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            return redirect('login')  # Redirect to login page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')  # Redirect after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    # user=User.object.get(id=request.user)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'user': request.user
    })
@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove if quantity is 0

    return redirect('view_cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        # For now, just clear the cart after "checkout"
        cart_items.delete()
        return render(request, 'checkout_success.html')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
