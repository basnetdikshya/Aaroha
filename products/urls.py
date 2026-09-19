from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.product_list,
        name='products'
    ),

    path(
        'inventory/',
        views.inventory,
        name='inventory'
    ),

    path(
        'inventory/update/<int:pk>/',
        views.update_stock,
        name='update_stock'
    ),

    path(
        '<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),
]