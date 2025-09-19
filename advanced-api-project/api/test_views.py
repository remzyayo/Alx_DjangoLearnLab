from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Unit tests for the Book API endpoints:
    - CRUD operations
    - Filtering, searching, and ordering
    - Permissions and authentication
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create an author
        self.author = Author.objects.create(name="Chinua Achebe")

        # Create some books
        self.book1 = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=self.author
        )
        self.book2 = Book.objects.create(
            title="No Longer at Ease", publication_year=1960, author=self.author
        )

        # API client
        self.client = APIClient()

        # Endpoints
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book1.id})
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update")
        self.delete_url = reverse("book-delete")

    # --- CRUD TESTS ---

    def test_list_books(self):
        """Anyone can view the list of books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_book_detail(self):
        """Anyone can view book details"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    def test_create_book_requires_authentication(self):
        """Unauthenticated users cannot create books"""
        data = {"title": "Arrow of God", "publication_year": 1964, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_book(self):
        """Authenticated users can create books"""
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "Arrow of God", "publication_year": 1964, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Arrow of God")

    def test_authenticated_user_can_update_book(self):
        """Authenticated users can update books"""
        self.client.login(username="testuser", password="testpass123")
        data = {"id": self.book1.id, "title": "Updated Title", "publication_year": 1959, "author": self.author.id}
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_authenticated_user_can_delete_book(self):
        """Authenticated users can delete books"""
        self.client.login(username="testuser", password="testpass123")
        data = {"id": self.book2.id}
        response = self.client.post(self.delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # --- FILTERING, SEARCHING, ORDERING ---

    def test_filter_books_by_publication_year(self):
        response = self.client.get(self.list_url, {"publication_year": 1958})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Things Fall Apart")

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {"search": "Things"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Things Fall Apart")

    def test_order_books_by_year_descending(self):
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "No Longer at Ease")