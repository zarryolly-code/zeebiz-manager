from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from customers import views


def manifest(request):
    return JsonResponse({
        "name": "ZeeBiz Manager",
        "short_name": "ZeeBiz",
        "description": "Manage customers, services, quotations, invoices, payments and business reports.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#1F4E79",
        "orientation": "portrait-primary",
        "icons": [
            {
                "src": "/static/icons/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("manifest.json", manifest, name="manifest"),

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