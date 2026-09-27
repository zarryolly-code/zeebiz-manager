from django.db import models
from businesses.models import Business

class UsageCounter(models.Model):

    business = models.OneToOneField(
        Business,
        on_delete=models.CASCADE,
        related_name="usage_counter"
    )

    quotation_count = models.PositiveIntegerField(
        default=0
    )

    quotation_year = models.PositiveIntegerField(
        default=0
    )

    quotation_month = models.PositiveIntegerField(
        default=0
    )

    invoice_count = models.PositiveIntegerField(
        default=0
    )

    invoice_year = models.PositiveIntegerField(
        default=0
    )

    invoice_month = models.PositiveIntegerField(
        default=0
    )

    receipt_count = models.PositiveIntegerField(
        default=0
    )

    receipt_year = models.PositiveIntegerField(
        default=0
    )

    receipt_month = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"Usage - {self.business.name}"

    from .usage_records import DocumentUsage