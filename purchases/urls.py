from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.purchase_list,
        name='purchase_list'
    ),

    path(
        'add/',
        views.add_purchase,
        name='add_purchase'
    ),

    path(
        'detail/<int:pk>/',
        views.purchase_detail,
        name='purchase_detail'
    ),

     path(
    'detail/<int:pk>/',
    views.purchase_detail,
    name='purchase_detail'
    ),

    path( 'update-status/<int:pk>/', views.update_purchase_status, name='update_purchase_status' ),

    path( 'edit/<int:pk>/', views.edit_purchase, name='edit_purchase' ),

    path( 'delete/<int:pk>/', views.delete_purchase, name='delete_purchase' ),
]