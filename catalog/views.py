from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render

from catalog.forms import BookForm
from catalog.models import Book

# ----- Data Delivery ----- (Mengirim data ke klien)
def book_json(request):
    data = Book.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), 
        content_type="application/json", 
    )

def book_xml(request):
    data = Book.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data), 
        content_type="application/xml", 
    )

def book_json_by_id(request, book_id):
    data = Book.objects.filter(pk=book_id) # Filter, bukan GET --> Tetap QuerySet
    if not data.exists():
        return HttpResponse(status=404)
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json",
    )

def book_xml_by_id(request, book_id):
    data = Book.objects.filter(pk=book_id) # Filter, bukan GET --> Tetap QuerySet
    if not data.exists():
        return HttpResponse(status=404)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml",
    )

def book_xml_download(request):
    data = Book.objects.all()
    response = HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml",
    )
    response["Content-Disposition"] = 'attachment; filename="books.xml"'
    return response

# ----- CRUD -----
def book_list(request):
    # Ambil data lewat endpoint JSON, lalu ubah kembali jadi objek BOOK
    json_response = book_json(request)
    books = [
        item.object
        for item in serializers.deserialize("json", json_response.content.decode("utf-8"))
    ]

    context = {"books" : books}
    return render(request, "book_list.html", context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "book_detail.html", {"book" : book})

def book_create(request):
    form = BookForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Buku berhasil ditambahkan!")
        return redirect("catalog:book_list")

    return render(request, "book_form.html", {"form": form, "is_edit": False})

def book_update(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    form = BookForm(request.POST or None, instance=book) # Instance = data lama

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Buku berhasil diperbarui!")
        return redirect("catalog:book_detail", book_id=book.id)
    
    return render(request, "book_form.html", {"form": form, "is_edit": True, "book":book})

def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        book.delete()
        messages.success(request, "Buku berhasil dihapus!")
        return redirect("catalog:book_list")

    return render(request, "book_delete.html", {"book": book})

def book_import(request):
    error = None

    if request.method == "POST":
        payload = request.POST.get("payload", "").strip()

        if not payload:
            error = "Data XML tidak boleh kosong"
        else:
            try:
                objects = list(serializers.deserialize("xml", payload))
                for obj in objects:
                    obj.save()
            except Exception:
                error = "Data XML tidak valid. Pastikan formatnya sesuai hasil dari /xml/ "
            else:
                messages.success(request, f"{len(objects)} buku berhasil diimpor!")
                return redirect("catalog:book_list")

    return render(request, "book_import.html", {"error": error})