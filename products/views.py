from django.shortcuts import render,get_object_or_404
from .models import Product


def product_list(request):
    products = Product.objects.filter(is_available=True)

    return render(
        request,
        'pages/products.html',
        {'products': products}
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