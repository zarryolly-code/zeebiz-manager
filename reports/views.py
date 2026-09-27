from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from businesses.models import Business
from customers.models import Customer
from quotations.models import Quotation
from invoices.models import Invoice
from receipts.models import Receipt


@login_required
def reports_dashboard(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    customers_count = Customer.objects.filter(
        business=business
    ).count()

    quotations = Quotation.objects.filter(
        business=business
    )

    invoices = Invoice.objects.filter(
        business=business
    )

    receipts = Receipt.objects.filter(
        business=business
    )

    quotations_count = quotations.count()
    invoices_count = invoices.count()
    receipts_count = receipts.count()

    quotation_total = sum(
        (q.total or Decimal("0.00") for q in quotations),
        Decimal("0.00")
    )

    invoice_total = sum(
        (i.total or Decimal("0.00") for i in invoices),
        Decimal("0.00")
    )

    amount_received = sum(
        (r.amount_paid or Decimal("0.00") for r in receipts),
        Decimal("0.00")
    )

    invoice_amount_paid = sum(
        (i.amount_paid or Decimal("0.00") for i in invoices),
        Decimal("0.00")
    )

    invoice_balance = invoice_total - amount_received
    quotation_amount_paid = sum(
        (r.amount_paid or Decimal("0.00") for r in receipts),
        Decimal("0.00")
    )

    quotation_balance = quotation_total - quotation_amount_paid

    context = {
        "business": business,

        "customers_count": customers_count,
        "quotations_count": quotations_count,
        "invoices_count": invoices_count,
        "receipts_count": receipts_count,

        "quotation_total": quotation_total,
        "invoice_total": invoice_total,
        "amount_received": amount_received,

        "invoice_balance": max(
            invoice_balance,
            Decimal("0.00")
        ),

        "quotation_balance": max(
            quotation_balance,
            Decimal("0.00")
        ),
    }

    return render(
        request,
        "reports_dashboard.html",
        context
    )