from django.utils import timezone
from .models import UsageCounter
from .usage_records import DocumentUsage

PLAN_LIMITS = {"Free": {"quotation": 2, "invoice": 2, "receipt": 2}, "Starter": {"quotation": 30, "invoice": 30, "receipt": 30}, "Business": {"quotation": 200, "invoice": 200, "receipt": 200}, "Premium": {"quotation": None, "invoice": None, "receipt": None}}

def get_usage_counter(business): counter, _ = UsageCounter.objects.get_or_create(business=business); now = timezone.now(); [(setattr(counter, f"{kind}_count", 0), setattr(counter, f"{kind}_year", now.year), setattr(counter, f"{kind}_month", now.month)) for kind in ("quotation", "invoice", "receipt") if getattr(counter, f"{kind}_year") != now.year or getattr(counter, f"{kind}_month") != now.month]; counter.save(); return counter

def can_create_document(business, document_type): subscription = business.subscription; limit = PLAN_LIMITS.get(subscription.plan, PLAN_LIMITS["Free"]).get(document_type, 0); return True if limit is None else getattr(get_usage_counter(business), f"{document_type}_count") < limit

def record_document_usage(business, document_type): counter = get_usage_counter(business); field = f"{document_type}_count"; setattr(counter, field, getattr(counter, field) + 1); counter.save()

PLAN_LIMITS = {
    "Free": {
        "service": 2,
        "customer": 2,
        "quotation": 2,
        "invoice": 2,
        "receipt": 2,
    },
    "Starter": {
        "service": 30,
        "customer": 30,
        "quotation": 30,
        "invoice": 30,
        "receipt": 30,
    },
    "Business": {
        "service": 200,
        "customer": 200,
        "quotation": 200,
        "invoice": 200,
        "receipt": 200,
    },
    "Premium": {
        "service": None,
        "customer": None,
        "quotation": None,
        "invoice": None,
        "receipt": None,
    },
}

def can_create_document_permanent(business, document_type):
    subscription = business.subscription
    limit = PLAN_LIMITS.get(
        subscription.plan,
        PLAN_LIMITS["Free"]
    ).get(document_type, 0)

    if limit is None:
        return True

    current_usage = DocumentUsage.objects.filter(
        business=business,
        document_type=document_type,
        created_at__year=timezone.now().year,
        created_at__month=timezone.now().month,
    ).count()

    return current_usage < limit


def record_permanent_usage(business, document_type):
    DocumentUsage.objects.create(
        business=business,
        document_type=document_type
    )