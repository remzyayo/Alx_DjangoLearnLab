from django.db import models
from datetime import datetime 

# Create your models here.
# Author model: Represents a book author with a simple name field
class Author(models.Model):
    name = models.CharField(max_length=255)

    def _str_(self):
        return self.name


# Book model: Represents a book, linked to an Author
# One Author can have multiple Books (One-to-Many relationship)
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.title} ({self.publication_year})"