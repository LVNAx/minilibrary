from django.forms import ModelForm, DateInput, Textarea, TextInput, URLInput
from catalog.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "category",
            "synopsis",
            "pages",
            "cover_url",
            "is_available",
            "published_at",
        ]

        labels = {
            "title": "Judul buku",
            "author": "Penulis",
            "category": "Kategori",
            "synopsis": "Sinopsis",
            "pages": "Halaman",
            "cover_url": "Url sampul",
            "is_available": "Tersedia",
            "published_at": "Tanggal terbit",
        }

        """
            Seperti namanya di sini, ia adalah Widget dari sebuah aplikasi-nya yang di mana ia berfungsi sebagai jenis tampilan
            pada HTML nya nanti. Contohnya nih:
                - TextInput itu yang 1 baris aja, 
                - TextAre itu yang kayak deskripsi dan juga panjang,
                - DateInput artinya yang pakai tanggal, dst.        
        """
        widgets = {
            "title": TextInput(attrs={"placeholder": "Laskar Pelangi"}),
            "author": TextInput(attrs={"placeholder": "Nugraha"}),
            "synopsis": Textarea(attrs={"placeholder": "Gw lapar", "rows": 4}),
            "cover_url": URLInput(attrs={"placeholder": "https://contoh.com"}),
            "published_at": DateInput(format="%Y-%m-%d", attrs={"type":"date"}),
        }