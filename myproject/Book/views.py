from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import BookForm
from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "Book/book_list.html"
    context_object_name = "books"
    ordering = ["title"]


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "Book/book_form.html"
    success_url = reverse_lazy("book:list")


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "Book/book_form.html"
    success_url = reverse_lazy("book:list")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "Book/book_confirm_delete.html"
    success_url = reverse_lazy("book:list")
