from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]
# Create router and register BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Keep the old list view (GET only)
    path('books/', BookList.as_view(), name='book-list'),

    # Include router-generated CRUD URLs
    path('', include(router.urls)),
]