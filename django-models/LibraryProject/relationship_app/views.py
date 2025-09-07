from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from .models import Book
from .models import Library

# ==========================
# Function-based view for listing all books
# ==========================

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ==========================
# Class-based view for displaying library details
# ==========================
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ==========================
# Authentication Views
# ==========================
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")  # redirect after register
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")  # redirect after login
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


# ==========================
# Role-Based Access Control Views
# ==========================

# Helpers to check roles

def admin_view(request):
    if request.user.profile.role == "Admin":
        return HttpResponse("Welcome, Admin!")
    return HttpResponseForbidden("You are not allowed to access this page.")

def librarian_view(request):
    if request.user.profile.role == "Librarian":
        return HttpResponse("Welcome, Librarian!")
    return HttpResponseForbidden("You are not allowed to access this page.")

def member_view(request):
    if request.user.profile.role == "Member":
        return HttpResponse("Welcome, Member!")
    return HttpResponseForbidden("You are not allowed to access this page.")


# Views restricted by role
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
