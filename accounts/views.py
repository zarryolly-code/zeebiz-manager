from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User

from customers.models import Customer
from businesses.models import Business
from quotations.models import Quotation
from subscriptions.models import Subscription
from usage_limits.views import can_create_document_permanent

import os
import resend

def business_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "business_login.html",
            {"error": "Invalid username or password."},
        )

    return render(request, "business_login.html")


@login_required
def dashboard(request):
    business = get_object_or_404(
        Business,
        owner=request.user
    )

    return render(
        request,
        "dashboard.html",
        {
            "business": business,
        },
    )


@login_required
def customers(request):
    business = get_object_or_404(
        Business,
        owner=request.user
    )

    all_customers = Customer.objects.filter(
        business=business
    ).order_by("name")

    return render(
        request,
        "customers.html",
        {
            "customers": all_customers,
            "business": business,
        },
    )


@login_required
def add_customer(request):
    business = get_object_or_404(Business, owner=request.user)

    if request.method == "POST":

        if not can_create_document_permanent(business, "customer"):
         return redirect("/subscription/plans/")
        subscription = business.subscription

        limits = {
            "Free": 2,
            "Starter": 30,
            "Business": 50,
            "Premium": None,
        }

        limit = limits.get(subscription.plan, 2)

        if limit is not None and Customer.objects.filter(business=business).count() >= limit:
            return redirect("/subscription/plans/")

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        Customer.objects.create(
            business=business,
            name=name,
            email=email,
            phone=phone,
            address=address,
        )

        return redirect("customers")

    return render(
        request,
        "add_customer.html",
        {"business": business},
    )


@login_required
def customer_detail(request, customer_id):
    business = get_object_or_404(
        Business,
        owner=request.user
    )

    customer = get_object_or_404(
        Customer,
        id=customer_id,
        business=business
    )

    service_records = customer.service_records.filter(
        business=business
    ).order_by("-service_date")

    quotations = customer.quotations.all()

    return render(
        request,
        "customer_detail.html",
        {
            "customer": customer,
            "service_records": service_records,
            "quotations": quotations,
            "business": business,
        },
    )


@login_required
def business_profile(request):
    business = get_object_or_404(
        Business,
        owner=request.user
    )

    if business.subscription.plan in ["Free", "Starter"]: return redirect("/subscription/plans/")

    if request.method == "POST":

        business.name = request.POST.get("name")
        business.tagline = request.POST.get("tagline")
        business.description = request.POST.get("description")
        business.email = request.POST.get("email")
        business.phone = request.POST.get("phone")
        business.address = request.POST.get("address")
        business.website = request.POST.get("website")

        business.primary_color = request.POST.get(
            "primary_color"
        ) or "#1F4E79"

        business.secondary_color = request.POST.get(
            "secondary_color"
        ) or "#F59E0B"

        if request.FILES.get("logo"):
            business.logo = request.FILES["logo"]

        business.save()

        return redirect("business_profile")

    return render(
        request,
        "business_profile.html",
        {
            "business": business,
        },
    )

def business_logout(request):
    logout(request)
    return redirect("business_login")

def business_register(request):
    if request.method == "POST":
        business_name = request.POST.get("business_name")
        owner_name = request.POST.get("owner_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        address = request.POST.get("address")

        if password != confirm_password:
            return render(
                request,
                "business_register.html",
                {"error": "Passwords do not match."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "business_register.html",
                {"error": "Username already exists."},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "business_register.html",
                {"error": "Email already exists."},
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=owner_name,
        )

        business = Business.objects.create(
            owner=user,
            name=business_name,
            address=address,
        )

        Subscription.objects.create(
            business=business,
            plan="Free",
        )

        resend.api_key = os.getenv("RESEND_API_KEY")

        try:
            resend.Emails.send({
            "from": "ZeeBiz Manager <onboarding@resend.dev>",
            "to": [email],
            "subject": "Welcome to ZeeBiz Manager",
            "html": f"<h2>Welcome to ZeeBiz Manager, {owner_name}!</h2><p>Your business account for <strong>{business_name}</strong> has been created successfully.</p><p>You can now log in and start managing your business.</p>",
        })
        except Exception:
            pass

        login(request, user)

        return redirect("dashboard")

    return render(
        request,
        "business_register.html",
    )