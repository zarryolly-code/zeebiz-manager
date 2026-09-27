from django.db import models
from customers.models import Customer
from businesses.models import Business


class ServiceRecord(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="service_records"
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="service_records",
        null=True,
        blank=True
    )

    service_name = models.CharField(max_length=200)
    service_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.service_name} - {self.customer.name}"