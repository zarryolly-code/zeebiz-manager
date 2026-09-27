from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from customers.models import Customer
from businesses.models import Business
from usage_limits.views import can_create_document_permanent

from .models import Invoice


def money_value(value):
    try:
        return Decimal(str(value or "0"))
    except (InvalidOperation, ValueError):
        return Decimal("0")


@login_required
def invoice_list(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    invoices = Invoice.objects.filter(
        business=business
    ).select_related(
        "customer"
    ).order_by(
        "-invoice_date"
    )

    total_invoices = invoices.count()

    total_paid = sum(
        (invoice.amount_paid for invoice in invoices),
        Decimal("0")
    )

    total_outstanding = sum(
        (invoice.balance for invoice in invoices),
        Decimal("0")
    )

    return render(
        request,
        "invoice_list.html",
        {
            "invoices": invoices,
            "business": business,
            "total_invoices": total_invoices,
            "total_paid": total_paid,
            "total_outstanding": total_outstanding,
        },
    )


@login_required
def invoice_create(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    customers = Customer.objects.filter(
        business=business
    ).order_by("name")

    if request.method == "POST":
        if not can_create_document_permanent(business, "invoice"):
          return redirect("invoice_list")
        subscription = business.subscription

        limits = {
            "Free": 2,
            "Starter": 30,
            "Business": 200,
            "Premium": None,
        }

        limit = limits.get(
            subscription.plan,
            2
        )

        if limit is not None:

            now = timezone.now()

            invoice_count = Invoice.objects.filter(
                business=business,
                created_at__year=now.year,
                created_at__month=now.month,
            ).count()

            if invoice_count >= limit:
                return redirect("invoice_list")

        customer_id = request.POST.get("customer")

        customer = get_object_or_404(
            Customer,
            id=customer_id,
            business=business,
        )

        subtotal = money_value(
            request.POST.get("subtotal")
        )

        discount = money_value(
            request.POST.get("discount")
        )

        total = subtotal - discount

        if total < 0:
            total = Decimal("0")

        amount_paid = money_value(
            request.POST.get("amount_paid")
        )

        if amount_paid < 0:
            amount_paid = Decimal("0")

        if amount_paid > total:
            amount_paid = total

        status = request.POST.get(
            "status"
        ) or "draft"

        invoice = Invoice.objects.create(
            business=business,
            customer=customer,
            invoice_number=request.POST.get(
                "invoice_number"
            ),
            due_date=request.POST.get(
                "due_date"
            ) or None,
            subtotal=subtotal,
            discount=discount,
            total=total,
            amount_paid=amount_paid,
            notes=request.POST.get(
                "notes"
            ),
            status=status,
        )

        return redirect(
            "invoice_detail",
            invoice_id=invoice.id
        )

    return render(
        request,
        "invoice_create.html",
        {
            "customers": customers,
            "business": business,
        },
    )


@login_required
def invoice_detail(request, invoice_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        business=business
    )

    return render(
        request,
        "invoice_detail.html",
        {
            "invoice": invoice,
            "business": business,
        },
    )


@login_required
def invoice_edit(request, invoice_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        business=business
    )

    customers = Customer.objects.filter(
        business=business
    ).order_by("name")

    if request.method == "POST":

        customer_id = request.POST.get("customer")

        customer = get_object_or_404(
            Customer,
            id=customer_id,
            business=business
        )

        subtotal = money_value(
            request.POST.get("subtotal")
        )

        discount = money_value(
            request.POST.get("discount")
        )

        total = subtotal - discount

        if total < 0:
            total = Decimal("0")

        amount_paid = money_value(
            request.POST.get("amount_paid")
        )

        if amount_paid < 0:
            amount_paid = Decimal("0")

        if amount_paid > total:
            amount_paid = total

        invoice.customer = customer

        invoice.invoice_number = request.POST.get(
            "invoice_number"
        )

        invoice.due_date = request.POST.get(
            "due_date"
        ) or None

        invoice.subtotal = subtotal

        invoice.discount = discount

        invoice.total = total

        invoice.amount_paid = amount_paid

        invoice.notes = request.POST.get(
            "notes"
        )

        invoice.status = request.POST.get(
            "status"
        ) or "draft"

        invoice.save()

        return redirect(
            "invoice_detail",
            invoice_id=invoice.id
        )

    return render(
        request,
        "invoice_edit.html",
        {
            "invoice": invoice,
            "customers": customers,
            "business": business,
        },
    )


@login_required
def invoice_delete(request, invoice_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        business=business
    )

    if request.method == "POST":

        invoice.delete()

        return redirect(
            "invoice_list"
        )

    return render(
        request,
        "invoice_delete.html",
        {
            "invoice": invoice,
            "business": business,
        },
    )