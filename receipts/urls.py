from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.receipt_list,
        name="receipt_list"
    ),

    path(
        "add/",
        views.receipt_create,
        name="receipt_create"
    ),

    path(
        "<int:receipt_id>/edit/",
        views.receipt_edit,
        name="receipt_edit"
    ),

    path(
    "<int:receipt_id>/",
    views.receipt_detail,
    name="receipt_detail"
),

path(
    "<int:receipt_id>/delete/",
    views.receipt_delete,
    name="receipt_delete"
),
]