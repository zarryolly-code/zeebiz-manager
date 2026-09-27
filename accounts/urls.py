from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.business_login, name="business_login"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("customers/", views.customers, name="customers"),
    path("customers/add/", views.add_customer, name="add_customer"),
    path(
        "customers/<int:customer_id>/",
        views.customer_detail,
        name="customer_detail",
    ),

    path("profile/", views.business_profile, name="business_profile"),

    path(
    "logout/",
    views.business_logout,
    name="logout"
),

path(
    "register/",
    views.business_register,
    name="business_register"
),
]