"""
relationship_app/query_samples.py

Contains sample ORM queries for:
1) Query all books by a specific author.
2) List all books in a library.
3) Retrieve the librarian for a library.

Run it either:
- As a script:       python relationship_app/query_samples.py
- From Django shell: python manage.py shell -c "from relationship_app.query_samples import run_examples; run_examples()"

If your project package is NOT 'Introduction_to_Django', change PROJECT_SETTINGS below.
"""

import os
import django

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# IMPORTANT: Set this to your actual project settings module if different.
PROJECT_SETTINGS = "Introduction_to_Django.settings"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def boot_django():
    """
    Ensure Django is set up when running this file directly as a script.
    If imported via manage.py shell, Django will already be configured.
    """
    from django.conf import settings
    if not settings.configured:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJECT_SETTINGS)
        django.setup()

# Ensure setup when run directly.
boot_django()

from relationship_app.models import Author, Book, Library, Librarian
from django.db.models import QuerySet


def books_by_author(author_name: str) -> QuerySet:
    """
    Returns a QuerySet of Book for a given author name.
    """
    return Book.objects.filter(author__name=author_name)


def books_in_library(library_name: str) -> QuerySet:
    """
    Returns a QuerySet of Book that are in the given library.
    """
    return Book.objects.filter(libraries__name=library_name).distinct()


def librarian_for_library(library_name: str):
    """
    Returns the Librarian instance for a given library name, or None if absent.
    """
    return Librarian.objects.filter(library__name=library_name).select_related("library").first()


def run_examples():
    """
    Helper to demonstrate the queries (prints results).
    Adjust names as needed to match your seeded data.
    """
    author_name = "Chinua Achebe"
    library_name = "Main Library"

    print(f"\n[1] All books by author: {author_name}")
    for b in books_by_author(author_name):
        print(f" - {b.title} (Author: {b.author.name})")

    print(f"\n[2] All books in library: {library_name}")
    for b in books_in_library(library_name):
        print(f" - {b.title} (Author: {b.author.name})")

    print(f"\n[3] Librarian for library: {library_name}")
    libn = librarian_for_library(library_name)
    if libn:
        print(f" - {libn.name}")
    else:
        print(" - No librarian assigned.")


if _name_ == "_main_":
    run_examples()