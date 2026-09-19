
from django.db import models


class Supplier(models.Model):

    name = models.CharField(
        max_length=150
    )

    company_name = models.CharField(
        max_length=150,
        blank=True
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
        ],
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

