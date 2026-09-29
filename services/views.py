from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import ServiceRecord
from customers.models import Customer
from businesses.models import Business
from usage_limits.views import can_create_document_permanent


@login_required
def service_list(request):
    business = get_object_or_404(
        Business,
        owner=request.user
    )

    service_records = ServiceRecord.objects.filter(
        business=business
    ).select_related("customer").order_by("-service_date")

    return render(
        request,
        "service_list.html",
        {
            "service_records": service_records,
            "business": business,
        },
    )


@login_required 
def add_service(request):
    business = get_object_or_404(Business, owner=request.user)

    customers = Customer.objects.filter(business=business).order_by("name")

    if request.method == "POST":

        if not can_create_document_permanent(business, "service"):
         return redirect("/subscription/plans/")
        subscription = business.subscription

        limits = {
            "Free": 2,
            "Starter": 50,
            "Business": 100,
            "Premium": None,
        }

        limit = limits.get(subscription.plan, 2)

        if limit is not None and ServiceRecord.objects.filter(business=business).count() >= limit:
            return redirect("/subscription/plans/")

        customer_id = request.POST.get("customer")
        service_name = request.POST.get("service_name")
        service_date = request.POST.get("service_date")
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        customer = get_object_or_404(
            Customer,
            id=customer_id,
            business=business,
        )

        ServiceRecord.objects.create(
            business=business,
            customer=customer,
            service_name=service_name,
            service_date=service_date,
            amount=amount,
            description=description,
        )

        return redirect("service_list")

    return render(
        request,
        "add_service.html",
        {
            "customers": customers,
            "business": business,
        },
    )