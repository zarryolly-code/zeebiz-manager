from django.shortcuts import redirect
from django.utils import timezone

from .views import can_create_document, record_document_usage, can_create_document_permanent, record_permanent_usage
from .usage_records import DocumentUsage
from quotations.models import Quotation
from invoices.models import Invoice
from receipts.models import Receipt
from services.models import ServiceRecord
from customers.models import Customer


class UsageLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        document_type = None

        if (
            request.method == "POST"
            and request.user.is_authenticated
            and request.resolver_match
        ):
            document_type = {
                "quotation_create": "quotation",
                "invoice_create": "invoice",
                "receipt_create": "receipt",
                "add_service": "service",
                "add_customer": "customer",
            }.get(request.resolver_match.url_name)

        business = getattr(request.user, "business", None)

        if document_type and business:

            counter = business.usage_counter

            if document_type in ("service", "customer"):

                if not can_create_document_permanent(
                    business,
                    document_type
                ):
                   
                   if document_type == "service":
                        return redirect("service_list")

                   return redirect("customers")

                return self.get_response(request)

            if document_type == "quotation":
                current_count = Quotation.objects.filter(
                    business=business,
                    created_at__year=timezone.now().year,
                    created_at__month=timezone.now().month,
                ).count()

            elif document_type == "invoice":
                current_count = Invoice.objects.filter(
                    business=business,
                    created_at__year=timezone.now().year,
                    created_at__month=timezone.now().month,
                ).count()

            else:
                current_count = Receipt.objects.filter(
                    business=business,
                    created_at__year=timezone.now().year,
                    created_at__month=timezone.now().month,
                ).count()

            field = f"{document_type}_count"
            year_field = f"{document_type}_year"
            month_field = f"{document_type}_month"

            now = timezone.now()

            if (
                getattr(counter, year_field) != now.year
                or getattr(counter, month_field) != now.month
            ):
                setattr(counter, field, 0)
                setattr(counter, year_field, now.year)
                setattr(counter, month_field, now.month)
                counter.save()

            if not can_create_document_permanent(business, document_type):
                return redirect(f"{document_type}_list")    

            if not can_create_document(business, document_type):
                return redirect(f"{document_type}_list")

            response = self.get_response(request)

            if response.status_code == 302:
                record_document_usage(business, document_type)

            return response

        return self.get_response(request)