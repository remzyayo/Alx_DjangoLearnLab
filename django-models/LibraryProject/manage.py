#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from relationship_app.models import CustomUser


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# Create Admin user
admin_user = CustomUser.objects.create_user(
    username="admin1",
    password="pass1234",
    role="Admin"
)

# Create Librarian user
librarian_user = CustomUser.objects.create_user(
    username="librarian1",
    password="pass1234",
    role="Librarian"
)

# Create Member user
member_user = CustomUser.objects.create_user(
    username="member1",
    password="pass1234",
    role="Member"
)

print(f"Created users:")
print(f"Admin: {admin_user.username}, role: {admin_user.role}")
print(f"Librarian: {librarian_user.username}, role: {librarian_user.role}")
print(f"Member: {member_user.username}, role: {member_user.role}")


if __name__ == '__main__':
    main()
