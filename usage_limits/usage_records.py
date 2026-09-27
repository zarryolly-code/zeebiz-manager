from django.db import models
from businesses.models import Business


DOCUMENT_TYPES = [
    ("service", "Service"),
    ("customer", "Customer"),
    ("quotation", "Quotation"),
    ("invoice", "Invoice"),
    ("receipt", "Receipt"),
]


class DocumentUsage(models.Model):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE
    )

    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.business.name} - {self.document_type}"