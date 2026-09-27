from django.db import models
from customers.models import Customer
from businesses.models import Business


class Quotation(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="quotations"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="quotations"
    )

    quotation_number = models.CharField(
        max_length=50,
        unique=True
    )

    quotation_date = models.DateField(
        auto_now_add=True
    )

    valid_until = models.DateField(
        null=True,
        blank=True
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.quotation_number

    @property
    def subtotal(self):
        return sum(
            item.total
            for item in self.items.all()
        )

    @property
    def total(self):
        return self.subtotal - self.discount


class QuotationItem(models.Model):
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items"
    )

    service_name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return self.service_name