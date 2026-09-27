from django.db.models.signals import post_save
from django.dispatch import receiver

from businesses.models import Business
from quotations.models import Quotation
from invoices.models import Invoice
from receipts.models import Receipt
from services.models import ServiceRecord
from customers.models import Customer

from .usage_records import DocumentUsage


@receiver(post_save, sender=Quotation)
def quotation_created(sender, instance, created, **kwargs):
    if created:
        DocumentUsage.objects.create(
            business=instance.business,
            document_type="quotation"
        )


@receiver(post_save, sender=Invoice)
def invoice_created(sender, instance, created, **kwargs):
    if created:
        DocumentUsage.objects.create(
            business=instance.business,
            document_type="invoice"
        )


@receiver(post_save, sender=Receipt)
def receipt_created(sender, instance, created, **kwargs):
    if created:
        DocumentUsage.objects.create(
            business=instance.business,
            document_type="receipt"
        )

@receiver(post_save, sender=ServiceRecord)
def service_created(sender, instance, created, **kwargs):

    if created and instance.business:

        DocumentUsage.objects.create(
            business=instance.business,
            document_type="service"
        )


@receiver(post_save, sender=Customer)
def customer_created(sender, instance, created, **kwargs):

    if created:

        DocumentUsage.objects.create(
            business=instance.business,
            document_type="customer"
        )
