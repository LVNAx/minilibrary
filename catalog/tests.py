from django.test import TestCase
from django.urls import reverse
from catalog.models import Book

class BookTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Laskar Pelangi", author="Andrea Hirata", category="fiksi",
            synopsis="Kisah anak Belitung.", pages=529, published_at="2005-09-01",
        )
        return super().setUp()

    def test_book_url(self):
        response = self.client.get(reverse("catalog:book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_list.html")

    def test_book_appears(self):
        response = self.client.get(reverse("catalog:book_list"))
        self.assertContains(response, "Laskar")
        self.assertContains(response, "Andrea")
        self.assertContains(response, "Fiksi")

    def test_empty_state(self):
        Book.objects.all().delete()
        response = self.client.get(reverse("catalog:book_list"))

        self.assertContains(response, "Belum ada buku")
        self.assertNotContains(response, "Laskar Pelangi")

    def test_model(self):
        self.assertEqual(str(self.book), "Laskar Pelangi")
        self.assertTrue(self.book.is_thick)

    def test_create_book(self):
        response = self.client.post(reverse("catalog:book_create"), {
            "title": "Bumi", "author": "Tere Liye", "category": "fiksi",
            "synopsis": "Petualangan.", "pages": 440,
            "cover_url": "", "is_available": "on", "published_at": "2014-01-01",
        })

        self.assertEqual(Book.objects.count(), 2)
        self.assertRedirects(response, reverse("catalog:book_list"))

    def test_update_book(self):
        self.client.post(reverse("catalog:book_update", args=[self.book.id]), {
            "title": "Judul Baru", "author": "Andrea Hirata", "category": "fiksi",
            "synopsis": "Kisah anak Belitung.", "pages": 529, "published_at": "2005-09-01",
        })

        self.book.refresh_from_db() # wajibm jadi ambil ulang dari DB

        self.assertEqual(self.book.title, "Judul Baru")
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book(self):
        self.client.post(reverse("catalog:book_delete", args=[self.book.id]))
        self.assertEqual(Book.objects.count(), 0)