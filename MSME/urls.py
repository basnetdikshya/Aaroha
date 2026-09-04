from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def products(request):
    return render(request, 'pages/products.html')


def categories(request):
    return render(request, 'pages/categories.html')


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


def login_view(request):
    return render(request, 'accounts/login.html')

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
    path('products/', products, name='products'),

    path('categories/', categories, name='categories'),

    path('about/', about, name='about'),

    path('contact/', contact, name='contact'),

    path('login/', login_view, name='login'),
]