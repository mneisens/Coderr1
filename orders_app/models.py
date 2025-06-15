from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField  # alternativ JSONField

class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    customer_user  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       related_name='orders_as_customer',
                                       on_delete=models.CASCADE)
    business_user  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       related_name='orders_as_business',
                                       on_delete=models.CASCADE)
    title                = models.CharField(max_length=255)
    revisions            = models.PositiveIntegerField()
    delivery_time_in_days= models.PositiveIntegerField()
    price                = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)

    offer_type           = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} – {self.title}"
