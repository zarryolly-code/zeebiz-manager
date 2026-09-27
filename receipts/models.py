from django.db import models
from customers.models import Customer
from businesses.models import Business


class Receipt(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("transfer", "Bank Transfer"),
        ("pos", "POS"),
        ("card", "Card"),
        ("other", "Other"),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="receipts"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="receipts"
    )

    quotation = models.ForeignKey(
    "quotations.Quotation",
    on_delete=models.SET_NULL,
    related_name="receipts",
    null=True,
    blank=True
)

    receipt_number = models.CharField(
        max_length=50,
        unique=True
    )

    receipt_date = models.DateField(
        auto_now_add=True
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="transfer"
    )

    description = models.TextField(
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.receipt_number