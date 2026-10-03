from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required

def home(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', '')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    if sort == 'low':
        products = products.order_by('price')
    elif sort == 'high':
        products = products.order_by('-price')

    return render(request, 'home.html', {
        'products': products,
        'query': query,
        'category': category,
        'sort': sort
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'product_detail.html', {
        'product': product
    })

def add_to_wishlist(request, id):
    wishlist = request.session.get('wishlist', [])

    if str(id) not in wishlist:
        wishlist.append(str(id))

    request.session['wishlist'] = wishlist

    return redirect('product_detail', id=id)

def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})
    current_quantity = cart.get(str(id), 0)

    if current_quantity < product.stock:
        cart[str(id)] = current_quantity + 1

    request.session['cart'] = cart

    return redirect('cart')

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')


def update_cart(request, id):

    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})

    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart.pop(str(id), None)

    elif quantity <= product.stock:
        cart[str(id)] = quantity

    else:
        # Maximum available stock
        cart[str(id)] = product.stock

    request.session['cart'] = cart

    return redirect('cart')

def cart(request):
    cart_data = request.session.get('cart', {})
    products = []

    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity
        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    from django.contrib.auth.forms import AuthenticationForm

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def checkout(request):

    cart_data = request.session.get('cart', {})

    if not cart_data:
        return redirect('cart')

    total = 0
    items = []

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(Product, id=product_id)

        # Check stock before order
        if quantity > product.stock:
            return redirect('cart')

        item_total = product.price * quantity
        total += item_total

        items.append({
            'product': product,
            'quantity': quantity,
            'price': product.price
        })

    if request.method == 'POST':

        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user,
            total_price=total,
            payment_method=payment_method
        )

        for item in items:

            product = item['product']
            quantity = item['quantity']

            # Reduce stock
            product.stock -= quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item['price']
            )

        request.session['cart'] = {}

        return render(request, 'order_success.html', {
            'order': order
        })

    return render(request, 'checkout.html', {
        'total': total
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })


@login_required
def cancel_order(request, id):
    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()

    return redirect('my_orders') 

@login_required
def wishlist(request):
    wishlist_data = request.session.get('wishlist', [])

    products = Product.objects.filter(id__in=wishlist_data)

    return render(request, 'wishlist.html', {
        'products': products
    })    

@login_required
def remove_from_wishlist(request, id):
    wishlist = request.session.get('wishlist', [])

    if str(id) in wishlist:
        wishlist.remove(str(id))

    request.session['wishlist'] = wishlist

    return redirect('wishlist')    

@login_required
def clear_order_history(request):
    if request.method == "POST":
        Order.objects.filter(user=request.user).delete()

    return redirect('my_orders')    