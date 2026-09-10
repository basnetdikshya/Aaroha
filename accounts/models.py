from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('rider', 'Delivery Rider'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    def _str_(self):
        return "{self.user.username} - {self.get_role_display()}"