from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile



def product_list(request):
   
    products = Product.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        'pages/products.html',
        {
            'products': products,
        }
    )
def product_detail(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        is_available=True
    )

    return render(
        request,
        'pages/product_detail.html',
        {'product': product}
    )

@login_required
def inventory(request):

    # Superuser can access
    if request.user.is_superuser:
        products = Product.objects.all().order_by('name')

    else:

        # Check user role
        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:
            return redirect('login')

        # Only owner and staff can access inventory
        if profile.role not in ['owner', 'staff']:
            return redirect('login')

        products = Product.objects.all().order_by('name')

    # Inventory statistics
    total_products = products.count()

    in_stock = products.filter(
        stock__gt=10
    ).count()

    low_stock = products.filter(
        stock__gt=0,
        stock__lte=10
    ).count()

    out_of_stock = products.filter(
        stock=0
    ).count()

    context = {
        'products': products,
        'total_products': total_products,
        'in_stock': in_stock,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
    }

    return render(
        request,
        'products/inventory.html',
        context
    )

def update_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        stock = request.POST.get('stock')

        if stock:
            product.stock = stock
            product.save()

        return redirect('inventory')

    return render(request, 'pages/update_stock.html', {
        'product': product
    })

    # =========================================================
# UPDATE PRODUCT STOCK
# =========================================================

@login_required
def update_stock(request, pk):

    # Superuser can access
    if request.user.is_superuser:
        pass

    else:

        # Get user profile
        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:
            return redirect('login')

        # Only owner and staff can update stock
        if profile.role not in ['owner', 'staff']:
            return redirect('login')

    # Get selected product
    product = get_object_or_404(
        Product,
        pk=pk
    )

    # Update stock after form submission
    if request.method == 'POST':

        new_stock = request.POST.get('stock', '').strip()

        if new_stock.isdigit():

            product.stock = int(new_stock)
            product.save()

            return redirect('inventory')

        error = 'Please enter a valid stock quantity.'

        return render(
            request,
            'products/update_stock.html',
            {
                'product': product,
                'error': error,
            }
        )

    return render(
        request,
        'products/update_stock.html',
        {
            'product': product,
        }
    )