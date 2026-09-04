from django.urls import path
from . import views


urlpatterns = [

    # Login
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # Logout
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Owner
    path(
        'owner/',
        views.owner_dashboard,
        name='owner_dashboard'
    ),

    # Staff
    path(
        'staff/',
        views.staff_dashboard,
        name='staff_dashboard'
    ),

    # Customer
    path(
        'customer/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),

    # Supplier
    path(
        'supplier/',
        views.supplier_dashboard,
        name='supplier_dashboard'
    ),

    # Delivery Rider
    path(
        'rider/',
        views.rider_dashboard,
        name='rider_dashboard'
    ),
]