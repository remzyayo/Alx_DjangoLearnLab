from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.


# Function-based view for listing all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {"books": books})


# Class-based view for displaying library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"