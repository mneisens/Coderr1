from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Offer(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='offers',
                                    on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    image       = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer #{self.pk} – {self.title}"

class OfferDetail(models.Model):
    OFFER_TYPE_CHOICES = [
        ('basic',    'Basic'),
        ('standard', 'Standard'),
        ('premium',  'Premium'),
    ]

    offer                 = models.ForeignKey(Offer,
                                              related_name='details',
                                              on_delete=models.CASCADE)
    title                 = models.CharField(max_length=255)
    revisions             = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price                 = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)

    offer_type            = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return f"Detail #{self.pk} for Offer #{self.offer_id}"
