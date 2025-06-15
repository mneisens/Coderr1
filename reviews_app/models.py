from django.conf import settings
from django.db import models

class Review(models.Model):
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reviews_received',
        on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reviews_given',
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # stellt sicher, dass pro (revisor, business_user) nur eine Bewertung existiert
        unique_together = [['business_user', 'reviewer']]

    def __str__(self):
        return f"Review {self.pk}: {self.reviewer} → {self.business_user}"
