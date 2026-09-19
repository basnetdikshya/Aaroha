
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Order, OrderItem
from products.models import Product


# =========================================================
# CHECKOUT
# =========================================================

@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0

    # Prepare cart items for checkout page
    for product_id, quantity in cart.items():

        product = Product.objects.get(
            id=product_id
        )

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':

        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')

        # -------------------------------------------------
        # CHECK STOCK AND CREATE ORDER SAFELY
        # -------------------------------------------------

        with transaction.atomic():

            locked_products = {}

            # Lock products while checking stock
            for product_id, quantity in cart.items():

                product = Product.objects.select_for_update().get(
                    id=product_id
                )

                locked_products[str(product_id)] = product

                # Not enough stock
                if quantity > product.stock:

                    return render(
                        request,
                        'orders/checkout.html',
                        {
                            'cart_items': cart_items,
                            'total': total,
                            'error': (
                                f'Not enough stock for '
                                f'{product.name}. '
                                f'Only {product.stock} '
                                f'{product.unit} available.'
                            ),
                        }
                    )

                # Product is unavailable
                if not product.is_available:

                    return render(
                        request,
                        'orders/checkout.html',
                        {
                            'cart_items': cart_items,
                            'total': total,
                            'error': (
                                f'{product.name} is currently '
                                f'not available.'
                            ),
                        }
                    )

            # -------------------------------------------------
            # CREATE ORDER
            # -------------------------------------------------

            order = Order.objects.create(
                user=request.user,
                customer_name=customer_name,
                phone=phone,
                address=address,
                city=city,
                total_amount=total,
            )

            # -------------------------------------------------
            # CREATE ORDER ITEMS + REDUCE STOCK
            # -------------------------------------------------

            for product_id, quantity in cart.items():

                product = locked_products[str(product_id)]

                subtotal = product.price * quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                    subtotal=subtotal,
                )

                # Reduce stock
                product.stock -= quantity
                product.save(update_fields=['stock'])

        # -------------------------------------------------
        # CLEAR CART AFTER SUCCESSFUL ORDER
        # -------------------------------------------------

        request.session['cart'] = {}
        request.session.modified = True

        return redirect(
            'order_success',
            order_id=order.id
        )

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(
        request,
        'orders/checkout.html',
        context
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

@login_required
def order_success(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_success.html',
        {'order': order}
    )


# =========================================================
# CUSTOMER ORDER HISTORY
# =========================================================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )


# =========================================================
# CUSTOMER ORDER DETAIL
# =========================================================

@login_required
def order_detail(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )


# =========================================================
# ORDER MANAGEMENT
# =========================================================

@login_required
def order_management(request):

    # Only superuser / owner / staff can manage orders

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = request.user.userprofile

        except Exception:
            return redirect('home')

        if profile.role not in ['owner', 'staff']:
            return redirect('home')

    # Get all orders, newest first
    orders = Order.objects.all().order_by('-created_at')

    # Send status choices to template
    status_choices = Order.STATUS_CHOICES

    return render(
        request,
        'orders/order_management.html',
        {
            'orders': orders,
            'status_choices': status_choices,
        }
    )


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

@login_required
def update_order_status(request, order_id):

    # Only superuser / owner / staff can update order status

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = request.user.userprofile

        except Exception:
            return redirect('home')

        if profile.role not in ['owner', 'staff']:
            return redirect('home')

    # Get the requested order
    order = get_object_or_404(
        Order,
        id=order_id
    )

    # Update status only through POST
    if request.method == 'POST':

        new_status = request.POST.get('status')

        # Get valid status values from Order model
        valid_statuses = [
            choice[0]
            for choice in Order.STATUS_CHOICES
        ]

        # Only save valid statuses
        if new_status in valid_statuses:

            order.status = new_status
            order.save()

    return redirect('order_management')

