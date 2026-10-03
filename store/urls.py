from django.urls import path
from .views import home, product_detail, add_to_cart, cart
from .views import add_to_wishlist
from .views import remove_from_cart, update_cart
from .views import register, login_view, logout_view
from .views import checkout
from .views import my_orders
from .views import wishlist
from .views import remove_from_wishlist
from .views import cancel_order
from .views import clear_order_history

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove-from-cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:id>/', update_cart, name='update_cart'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('checkout/', checkout, name='checkout'),
    path('my-orders/', my_orders, name='my_orders'),
    path('add-to-wishlist/<int:id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('remove-from-wishlist/<int:id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('cancel-order/<int:id>/', cancel_order, name='cancel_order'),
    path('clear-order-history/',clear_order_history, name='clear_order_history'),
]