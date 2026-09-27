from django.db import models

from businesses.models import Business


class Subscription(models.Model):
    business = models.OneToOneField(
        Business,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.CharField(max_length=50, default="Free")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=10,
        default="NGN"
    )

    start_date = models.DateField(auto_now_add=True)

    expiry_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.business.name} - {self.plan}"
