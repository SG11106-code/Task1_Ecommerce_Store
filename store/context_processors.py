def cart_count(request):
    cart = request.session.get('cart', {})
    wishlist = request.session.get('wishlist', [])

    return {
        'cart_count': sum(cart.values()),
        'wishlist_count': len(wishlist)
    }