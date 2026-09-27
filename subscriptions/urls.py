from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.subscription,
        name="subscription",
    ),

    path(
        "plans/",
        views.plans,
        name="plans",
    ),

    path(
        "choose/<str:plan_name>/",
        views.choose_plan,
        name="choose_plan",
    ),

    path(
        "pay/<str:plan_name>/",
        views.paystack_payment,
        name="paystack_payment",
    ),

    path(
        "payment/paystack/success/",
        views.paystack_success,
        name="paystack_success",
    ),
]