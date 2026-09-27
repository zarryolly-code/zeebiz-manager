from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.quotation_list,
        name="quotation_list"
    ),

    path(
        "add/",
        views.quotation_create,
        name="quotation_create"
    ),

    path(
        "<int:quotation_id>/",
        views.quotation_detail,
        name="quotation_detail"
    ),

    path(
    "<int:quotation_id>/edit/",
    views.quotation_edit,
    name="quotation_edit"
),

    path(
        "<int:quotation_id>/convert-to-invoice/",
        views.quotation_to_invoice,
        name="quotation_to_invoice"
    ),

    path(
    "<int:quotation_id>/delete/",
    views.quotation_delete,
    name="quotation_delete"
),

]