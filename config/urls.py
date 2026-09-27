from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from customers import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("accounts/", include("accounts.urls")),

    path(
        "accounts/services/",
        include("services.urls")
    ),

    path(
        "accounts/quotations/",
        include("quotations.urls")
    ),

    path(
        "receipts/",
        include("receipts.urls")
    ),

    path(
        "invoices/",
        include("invoices.urls")
    ),

    path(
        "reports/",
        include("reports.urls")
    ),

    path(
        "subscription/",
        include("subscriptions.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )