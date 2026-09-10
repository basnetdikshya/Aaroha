from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_list, name='products'),
    path(
        '<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),
]