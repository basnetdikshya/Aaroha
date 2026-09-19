from django.urls import path
from . import views


urlpatterns = [

    # Supplier list
    path(
        '',
        views.supplier_list,
        name='supplier_list'
    ),

    # Add supplier
    path(
        'add/',
        views.add_supplier,
        name='add_supplier'
    ),

    # Supplier details
    path(
        'detail/<int:pk>/',
        views.supplier_detail,
        name='supplier_detail'
    ),

    # Edit supplier
    path(
        'edit/<int:pk>/',
        views.edit_supplier,
        name='edit_supplier'
    ),

    # Delete supplier
    path(
        'delete/<int:pk>/',
        views.delete_supplier,
        name='delete_supplier'
    ),

]
