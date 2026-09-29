from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Receipt
from customers.models import Customer
from quotations.models import Quotation
from invoices.models import Invoice
from usage_limits.views import can_create_document_permanent


def money_value(value):
    try:
        return Decimal(str(value or "0"))
    except (InvalidOperation, ValueError):
        return Decimal("0.00")


@login_required
def receipt_list(request):

    business = request.user.business

    receipts = Receipt.objects.filter(
        business=business
    ).select_related(
        "quotation",
        "customer"
    ).order_by(
        "-created_at"
    )

    receipt_data = []

    for receipt in receipts:

        quotation_total = Decimal("0.00")
        balance = Decimal("0.00")

        if receipt.quotation:
            quotation_total = receipt.quotation.total
            balance = quotation_total - receipt.amount_paid

            if balance < 0:
                balance = Decimal("0.00")

        receipt_data.append({
            "receipt": receipt,
            "quotation_total": quotation_total,
            "balance": balance,
        })

    return render(
        request,
        "receipt_list.html",
        {
            "receipt_data": receipt_data,
            "business": business,
        },
    )


@login_required
def receipt_create(request):
    business = request.user.business

    customers = Customer.objects.filter(
        business=business
    ).order_by("name")

    quotations = Quotation.objects.filter(
        business=business
    ).order_by("-created_at")

    invoice_id = request.GET.get("invoice_id")

    invoice = None

    if invoice_id:
        invoice = get_object_or_404(
            Invoice,
            id=invoice_id,
            business=business
        )

    if request.method == "POST":
        if not can_create_document_permanent(business, "receipt"):
         return redirect("/subscription/plans/")
        subscription = business.subscription

        limits = {
            "Free": 2,
            "Starter": 30,
            "Business": 200,
            "Premium": None,
        }

        limit = limits.get(subscription.plan, 2)

        if limit is not None:
            now = timezone.now()

            receipt_count = Receipt.objects.filter(
                business=business,
                created_at__year=now.year,
                created_at__month=now.month,
            ).count()

            if receipt_count >= limit:
               return redirect("/subscription/plans/")

        customer_id = request.POST.get("customer")
        quotation_id = request.POST.get("quotation")
        posted_invoice_id = request.POST.get("invoice_id")

        if posted_invoice_id:
            invoice = get_object_or_404(
                Invoice,
                id=posted_invoice_id,
                business=business
            )

            customer = invoice.customer

            if invoice.quotation:
                quotation = invoice.quotation

        customer = get_object_or_404(
            Customer,
            id=customer_id,
            business=business,
        )

        quotation = None

        if quotation_id:
            quotation = get_object_or_404(
                Quotation,
                id=quotation_id,
                business=business,
            )

        Receipt.objects.create(
            business=business,
            invoice=invoice,
            quotation=quotation,
            customer=customer,
            receipt_number=f"RC-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            amount_paid=money_value(
                request.POST.get("amount_paid")
            ),
            payment_method=request.POST.get("payment_method") or "transfer",
            description=request.POST.get("description"),
            notes=request.POST.get("notes"),
        )

        return redirect("receipt_list")

    return render(
        request,
        "receipt_create.html",
        {
            "customers": customers,
            "quotations": quotations,
            "business": business,
            "invoice": invoice,
        },
    )

@login_required
def receipt_edit(request, receipt_id):

    business = request.user.business

    receipt = get_object_or_404(
        Receipt,
        id=receipt_id,
        business=business
    )

    customers = Customer.objects.filter(
        business=business
    ).order_by("name")

    quotations = Quotation.objects.filter(
        business=business
    ).order_by("-created_at")

    if request.method == "POST":

        customer_id = request.POST.get("customer")
        quotation_id = request.POST.get("quotation")

        receipt.customer = get_object_or_404(
            Customer,
            id=customer_id,
            business=business
        )

        receipt.quotation = None

        if quotation_id:
            receipt.quotation = get_object_or_404(
                Quotation,
                id=quotation_id,
                business=business
            )

        receipt.amount_paid = money_value(
            request.POST.get("amount_paid")
        )

        receipt.payment_method = request.POST.get(
            "payment_method"
        ) or "transfer"

        receipt.description = request.POST.get(
            "description"
        )

        receipt.notes = request.POST.get(
            "notes"
        )

        receipt.save()

        return redirect("receipt_list")

    quotation_total = Decimal("0.00")
    balance = Decimal("0.00")

    if receipt.quotation:

        quotation_total = receipt.quotation.total

        balance = quotation_total - receipt.amount_paid

        if balance < 0:
            balance = Decimal("0.00")

    return render(
        request,
        "receipt_edit.html",
        {
            "receipt": receipt,
            "customers": customers,
            "quotations": quotations,
            "business": business,
            "quotation_total": quotation_total,
            "balance": balance,
        },
    )


@login_required
def receipt_detail(request, receipt_id):

    business = request.user.business

    receipt = get_object_or_404(
        Receipt,
        id=receipt_id,
        business=business
    )

    quotation_total = Decimal("0.00")
    balance = Decimal("0.00")

    if receipt.quotation:

        quotation_total = receipt.quotation.total

        balance = quotation_total - receipt.amount_paid

        if balance < 0:
            balance = Decimal("0.00")

    return render(
        request,
        "receipt_detail.html",
        {
            "receipt": receipt,
            "business": business,
            "quotation_total": quotation_total,
            "balance": balance,
        },
    )

@login_required
def receipt_delete(request, receipt_id):

    business = request.user.business

    receipt = get_object_or_404(
        Receipt,
        id=receipt_id,
        business=business
    )

    if request.method == "POST":
        receipt.delete()

        return redirect(
            "receipt_list"
        )

    return render(
        request,
        "receipt_delete.html",
        {
            "receipt": receipt,
            "business": business,
        },
    )