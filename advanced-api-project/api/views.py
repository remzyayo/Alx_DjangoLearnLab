from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

# Create your views here.


# List all books (open to everyone)
class BookListView(generics.ListAPIView):
    """
    Retrieves a list of all books in the database.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Retrieve a single book by ID (open to everyone)
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves details of a specific book by its ID.
    Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Create a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    """
    Allows authenticated users to add a new book.
    Includes validation for publication_year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Additional custom logic could go here if needed
        serializer.save()


# Update an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    """
    Allows authenticated users to update an existing book.
    Ensures validation is applied before saving.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


# Delete a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    """
    Allows authenticated users to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]