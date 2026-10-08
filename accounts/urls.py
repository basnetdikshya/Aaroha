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

   path('manage-orders/', views.manage_orders, name='manage_orders'),
   path('manage-orders/<int:order_id>/', views.manage_order_detail, name='manage_order_detail'),
   path('sales/', views.sales_management, name='sales_management'),
   path( 'sales/<int:order_id>/',views.sales_detail,name='sales_detail'),
   path('customers/', views.customer_management, name='customer_management'),
   path('customers/<int:user_id>/',views.customer_detail,name='customer_detail'),
   path('customers/<int:customer_id>/toggle-status/',views.toggle_customer_status,name='toggle_customer_status'),
   path('riders/',views.rider_management,name='rider_management'),
   path('riders/add/',views.add_rider,name='add_rider'),
   path('riders/<int:rider_id>/toggle-status/',views.toggle_rider_status,name='toggle_rider_status'),
   path('riders/<int:rider_id>/edit/',views.edit_rider,name='edit_rider'),
]