from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name


class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)

    def _str_(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="books")

    def _str_(self):
        return f"{self.title} by {self.author.name}"


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")

    def _str_(self):
        return self.name
