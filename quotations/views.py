from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import Quotation, QuotationItem
from customers.models import Customer
from businesses.models import Business
from invoices.models import Invoice
from usage_limits.views import can_create_document, record_document_usage, can_create_document_permanent


@login_required
def quotation_list(request):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    quotations = Quotation.objects.filter(
        business=business
    ).order_by("-created_at")

    return render(
        request,
        "quotation_list.html",
        {
            "quotations": quotations,
            "business": business,
        },
    )


@login_required
def quotation_create(request):
    business = get_object_or_404(Business, owner=request.user)

    customers = Customer.objects.filter(
        business=business
    ).order_by("name")

    if request.method == "POST":
        if not can_create_document_permanent(business, "quotation"):
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

            quotation_count = Quotation.objects.filter(
                business=business,
                created_at__year=now.year,
                created_at__month=now.month,
            ).count()

            if quotation_count >= limit:
                return redirect("/subscription/plans/")

        customer_id = request.POST.get("customer")
        valid_until = request.POST.get("valid_until")
        discount = request.POST.get("discount") or 0
        notes = request.POST.get("notes")

        customer = get_object_or_404(
            Customer,
            id=customer_id,
            business=business,
        )

        if not valid_until:
            valid_until = (
                timezone.now().date() + timedelta(days=14)
            )

        quotation = Quotation.objects.create(
            business=business,
            customer=customer,
            quotation_number=f"QT-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            valid_until=valid_until,
            discount=discount,
            notes=notes,
        )

        service_names = request.POST.getlist("service_name")
        descriptions = request.POST.getlist("description")
        quantities = request.POST.getlist("quantity")
        unit_prices = request.POST.getlist("unit_price")

        for i in range(len(service_names)):
            if service_names[i].strip():
                QuotationItem.objects.create(
                    quotation=quotation,
                    service_name=service_names[i],
                    description=descriptions[i],
                    quantity=quantities[i] or 1,
                    unit_price=unit_prices[i] or 0,
                )

        return redirect("quotation_list")

    return render(
        request,
        "quotation_create.html",
        {
            "customers": customers,
            "business": business,
        },
    )


@login_required
def quotation_detail(
    request,
    quotation_id
):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    quotation = get_object_or_404(
        Quotation,
        id=quotation_id,
        business=business
    )

    return render(
        request,
        "quotation_detail.html",
        {
            "quotation": quotation,
            "business": business,
        },
    )


@login_required
def quotation_edit(request, quotation_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    quotation = get_object_or_404(
        Quotation,
        id=quotation_id,
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

        quotation.customer = customer

        quotation.quotation_number = request.POST.get(
            "quotation_number"
        )

        quotation.valid_until = request.POST.get(
            "valid_until"
        ) or None

        quotation.discount = request.POST.get(
            "discount"
        ) or 0

        quotation.notes = request.POST.get(
            "notes"
        )

        quotation.save()

        return redirect(
            "quotation_detail",
            quotation_id=quotation.id
        )

    return render(
        request,
        "quotation_edit.html",
        {
            "quotation": quotation,
            "customers": customers,
            "business": business,
        },
    )


@login_required
def quotation_to_invoice(
    request,
    quotation_id
):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    quotation = get_object_or_404(
        Quotation,
        id=quotation_id,
        business=business
    )

    # Check if this quotation already has an invoice.
    # If it does, open the existing invoice instead
    # of creating another one.

    existing_invoice = Invoice.objects.filter(
        quotation=quotation
    ).first()

    if existing_invoice:

        return redirect(
            "invoice_detail",
            invoice_id=existing_invoice.id
        )

    if not can_create_document_permanent(business, "invoice"):
        return redirect("/subscription/plans/")

    invoice = Invoice.objects.create(

        business=business,

        customer=quotation.customer,

        quotation=quotation,

        invoice_number=(
            f"INV-{quotation.quotation_number}"
        ),

        subtotal=quotation.subtotal,

        discount=quotation.discount,

        total=quotation.total,

        due_date=(
            timezone.now().date()
            + timedelta(days=14)
        ),

        amount_paid=0,

        status="draft",

        notes=(
            "Invoice created from quotation "
            f"{quotation.quotation_number}."
        ),
    )

    return redirect(
        "invoice_detail",
        invoice_id=invoice.id
    )


@login_required
def quotation_delete(request, quotation_id):

    business = get_object_or_404(
        Business,
        owner=request.user
    )

    quotation = get_object_or_404(
        Quotation,
        id=quotation_id,
        business=business
    )

    if request.method == "POST":
        quotation.delete()

        return redirect(
            "quotation_list"
        )

    return render(
        request,
        "quotation_delete.html",
        {
            "quotation": quotation,
            "business": business,
        },
    )