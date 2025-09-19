from django.shortcuts import render
from django.contrib import admin
from .models import Author
from .models import Book

# Create your views here.
admin.site.register(Author)
admin.site.register(Book)