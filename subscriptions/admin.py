from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "business",
        "plan",
        "start_date",
        "expiry_date",
        "is_active",
    )