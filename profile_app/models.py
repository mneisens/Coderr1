from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    CUSTOMER = 'customer'
    BUSINESS = 'business'
    TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (BUSINESS, 'Business'),
    ]

    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    type           = models.CharField(max_length=8, choices=TYPE_CHOICES)
    file           = models.ImageField(upload_to='profiles/', null=True, blank=True)
    location       = models.CharField(max_length=255, default='', blank=True)
    tel            = models.CharField(max_length=20,   default='', blank=True)
    description    = models.TextField(default='', blank=True)
    working_hours  = models.CharField(max_length=255, default='', blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.type})"
