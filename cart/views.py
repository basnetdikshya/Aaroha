from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


# def add_to_cart(request, product_id):

#     product = get_object_or_404(
#         Product,
#         id=product_id,
#         is_available=True
#     )

#     if request.method == 'POST':

#         quantity = int(
#             request.POST.get('quantity', 1)
#         )

#         cart = request.session.get('cart', {})

#         product_id = str(product_id)

#         if product_id in cart:
#             cart[product_id] += quantity
#         else:
#             cart[product_id] = quantity

#         request.session['cart'] = cart
#         request.session.modified = True

#     return redirect('cart')

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

        current_quantity = cart.get(product_id, 0)

        new_quantity = current_quantity + quantity

        # Check available stock
        if new_quantity > product.stock:

            request.session['cart_error'] = (
                f'Only {product.stock} '
                f'{product.unit} of {product.name} '
                f'is available.'
            )

            return redirect('cart')

        if new_quantity > 0:
            cart[product_id] = new_quantity

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')

# def cart_view(request):

#     cart = request.session.get('cart', {})

#     cart_items = []
#     total = 0

#     for product_id, quantity in cart.items():

#         product = get_object_or_404(
#             Product,
#             id=product_id
#         )

#         subtotal = product.price * quantity

#         total += subtotal

#         cart_items.append({
#             'product': product,
#             'quantity': quantity,
#             'subtotal': subtotal,
#         })

#     context = {
#         'cart_items': cart_items,
#         'total': total,
#     }

#     return render(
#         request,
#         'cart/cart.html',
#         context
#     )


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

    error = request.session.pop(
        'cart_error',
        None
    )

    context = {
        'cart_items': cart_items,
        'total': total,
        'error': error,
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


# def update_cart(request, product_id):

#     if request.method == 'POST':

#         quantity = int(
#             request.POST.get('quantity', 1)
#         )

#         cart = request.session.get('cart', {})

#         product_id = str(product_id)

#         if product_id in cart:

#             if quantity > 0:
#                 cart[product_id] = quantity
#             else:
#                 del cart[product_id]

#         request.session['cart'] = cart
#         request.session.modified = True

#     return redirect('cart')


def update_cart(request, product_id):

    if request.method == 'POST':

        quantity = int(
            request.POST.get('quantity', 1)
        )

        cart = request.session.get('cart', {})

        product_id = str(product_id)

        if product_id in cart:

            product = get_object_or_404(
                Product,
                id=product_id,
                is_available=True
            )

            if quantity > product.stock:

                request.session['cart_error'] = (
                    f'Only {product.stock} '
                    f'{product.unit} of {product.name} '
                    f'is available.'
                )

                return redirect('cart')

            if quantity > 0:
                cart[product_id] = quantity
            else:
                del cart[product_id]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')