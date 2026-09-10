from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    if request.method == 'POST':

        quantity = int(
            request.POST.get('quantity', 1)
        )

        cart = request.session.get('cart', {})

        product_id = str(product_id)

        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


def cart_view(request):

    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(
        request,
        'cart/cart.html',
        context
    )


def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')