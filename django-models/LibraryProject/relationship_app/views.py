
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from .forms import BookForm  # Make sure you have a BookForm for create/edit


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})



# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


#registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #Logs in the user automatically
            messages.success(request, "Registration Successful!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {'form':form})


#login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "logged in successful!")
                return redirect ("home")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {'form':form})


#logout view
def logout_view(request):
    logout (request)
    messages.info((request, "You have successfully logged out!"))
    return render(request, "relationship_app/logout.html")



# Helper functions to check user roles
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# Views restricted by roles
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# Create Book
@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "relationship_app/add_book.html", {"form": form})


# Edit Book
@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/edit_book.html", {"form": form, "book": book})


# Delete Book
@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "relationship_app/delete_book.html", {"book": book})
