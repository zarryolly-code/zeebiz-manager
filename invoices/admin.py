from django.contrib import admin

from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "business",
        "customer",
        "quotation",
        "invoice_date",
        "due_date",
        "total",
        "amount_paid",
        "status",
    )

    list_filter = (
        "status",
        "invoice_date",
        "due_date",
    )

    search_fields = (
        "invoice_number",
        "customer__name",
        "business__name",
    )