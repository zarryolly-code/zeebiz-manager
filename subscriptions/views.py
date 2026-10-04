from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from businesses.models import Business
import requests
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal
from subscriptions.models import Subscription


@login_required
def subscription(request):
    business = get_object_or_404(
        Business,
        owner=request.user
    )

    subscription = business.subscription

    return render(
        request,
        "subscription.html",
        {
            "business": business,
            "subscription": subscription,
        }
    )


def plans(request):
    return render(request, "plans.html")


def choose_plan(request, plan_name):
    prices = {
        "Starter": 7000,
        "Business": 12000,
        "Premium": 20000,
    }

    price = prices.get(plan_name, 0)

    return render(
        request,
        "choose_plan.html",
        {
            "plan_name": plan_name,
            "price": price,
        }
    )


@login_required
def paystack_payment(request, plan_name):
    prices = {
        "Starter": 7000,
        "Business": 12000,
        "Premium": 20000,
    }

    price = prices.get(plan_name)

    if not price:
        return redirect("plans")

    reference = (
        f"ZBIZ-{request.user.id}-{plan_name.upper()}-"
        f"{timezone.now().strftime('%Y%m%d%H%M%S')}"
    )

    payment_data = {
        "email": request.user.email,
        "amount": int(price * 100),
        "currency": "NGN",
        "reference": reference,
        "callback_url": request.build_absolute_uri(
            "/subscription/payment/paystack/success/"
        ),
        "metadata": {
            "plan_name": plan_name,
            "user_id": request.user.id,
        },
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        headers={
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        },
        json=payment_data,
    )

    data = response.json()

    if response.status_code == 200 and data.get("status"):
        payment_link = data.get("data", {}).get("authorization_url")

        if payment_link:
            return redirect(payment_link)

    return HttpResponse(
        f"Paystack response: {response.status_code}"
        f"<br><br>{data}"
    )


@login_required
def paystack_success(request):
    reference = request.GET.get("reference")

    if not reference:
        return redirect("subscription")

    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers={
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        },
    )

    data = response.json()

    if response.status_code != 200 or not data.get("status"):
        return redirect("subscription")

    transaction = data.get("data", {})

    if transaction.get("status") != "success":
        return redirect("subscription")

    if transaction.get("reference") != reference:
        return redirect("subscription")

    metadata = transaction.get("metadata", {})
    plan_name = metadata.get("plan_name")

    if not plan_name:
        return redirect("subscription")

    prices = {
        "Starter": Decimal("7000"),
        "Business": Decimal("12000"),
        "Premium": Decimal("20000"),
    }

    price = prices.get(plan_name)

    if not price:
        return redirect("subscription")

    paid_amount = Decimal(str(transaction.get("amount", 0))) / Decimal("100")

    if paid_amount < price:
        return redirect("subscription")

    subscription = get_object_or_404(
        Subscription,
        business__owner=request.user,
    )

    subscription.plan = plan_name
    subscription.price = price
    subscription.currency = "NGN"
    subscription.is_active = True
    subscription.start_date = timezone.now().date()
    subscription.save()

    return redirect("subscription")