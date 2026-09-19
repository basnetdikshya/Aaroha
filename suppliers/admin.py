from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'company_name',
        'phone',
        'email',
        'city',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'city',
    )

    search_fields = (
        'name',
        'company_name',
        'phone',
        'email',
    )

