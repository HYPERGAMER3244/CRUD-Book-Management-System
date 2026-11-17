from django.test import TestCase
from django.urls import reverse

from .models import Book


class BookCrudTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="The Hobbit",
            author="J. R. R. Tolkien",
            price=25,
        )

    def test_book_list_displays_books_and_add_link(self):
        response = self.client.get(reverse("book:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertContains(response, reverse("book:add"))

    def test_create_book(self):
        response = self.client.post(
            reverse("book:add"),
            {"title": "Dune", "author": "Frank Herbert", "price": 30},
        )

        self.assertRedirects(response, reverse("book:list"))
        self.assertTrue(Book.objects.filter(title="Dune").exists())

    def test_update_book(self):
        response = self.client.post(
            reverse("book:edit", args=[self.book.pk]),
            {"title": self.book.title, "author": self.book.author, "price": 35},
        )

        self.assertRedirects(response, reverse("book:list"))
        self.book.refresh_from_db()
        self.assertEqual(self.book.price, 35)

    def test_delete_requires_confirmation_and_post(self):
        delete_url = reverse("book:delete", args=[self.book.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse("book:list"))
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
