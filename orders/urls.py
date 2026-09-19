from django.urls import path
from . import views


urlpatterns = [

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'detail/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

        path(
        'management/',
        views.order_management,
        name='order_management'
    ),

    path(
        'management/update-status/<int:order_id>/',
        views.update_order_status,
        name='update_order_status'
    ),

]