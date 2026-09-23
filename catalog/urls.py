from django.urls import path
from catalog.views import (
    book_json,
    book_xml,
    book_json_by_id,
    book_xml_by_id,
    book_xml_download,
    book_list,
    book_detail,
    book_create,
    book_update,
    book_delete,
    book_import,
)

app_name = "catalog"

urlpatterns = [
    path("", book_list, name="book_list"),
    path("books/add/", book_create, name="book_create"),
    path("books/import/", book_import, name="book_import"),
    path("books/<uuid:book_id>/", book_detail, name="book_detail"),
    path("books/<uuid:book_id>/edit/", book_update, name="book_update"),
    path("books/<uuid:book_id>/delete/", book_delete, name="book_delete"),
    path("json/", book_json, name="book_json"),
    path("xml/", book_xml, name="book_xml"),
    path("xml/download/", book_xml_download, name="book_xml_download"),
    path("json/<uuid:book_id>", book_json_by_id, name="book_json_by_id"),
    path("xml/<uuid:book_id>", book_xml_by_id, name="book_xml_by_id"),        
]