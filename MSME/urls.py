from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from accounts import views  
from django.conf import settings
from django.conf.urls.static import static
from products.models import Category
from products.models import Product

def home(request):
    return render(request, 'index.html')


def products(request):

    products = Product.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        'pages/products.html',
        {'products': products}
    )


def categories(request):
    # return render(request, 'pages/categories.html')
    categories = Category.objects.all()

    return render(
        request,
        'pages/categories.html',
        {'categories': categories}
    )
def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')




urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),
    # path('products/', products, name='products'),
    path('products/', include('products.urls')),

    path('categories/', categories, name='categories'),

    path('about/', about, name='about'),

    path('contact/', contact, name='contact'),


    path('cart/', include('cart.urls')),

    path('orders/', include('orders.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)