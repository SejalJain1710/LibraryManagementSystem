from django.db import models
from django.contrib.auth.models import AbstractUser

    # a professional who facilitates access to information and resources within a library.
    # A library member is an authorized person who can use the library's facilities and enter the library
class Role(models.Model):
    class Role(models.TextChoices):
        LIBRARIAN = 'librarian'
        MEMBER = 'member'
    # add these roles in db and don't expose it to client
    name = models.CharField(max_length=50, choices=Role.choices, default=Role.MEMBER)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role, related_name='users')  # Users can have multiple roles (e.g., both Member and Librarian)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username 
    
class Book(models.Model):
    name = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    def __str__(self):
        return self.name

class BookCopy(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available'
        ISSUED = 'issued'

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    copy_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.AVAILABLE)

    def __str__(self):
        return self.book.name + ' - ' + self.copy_number
    
class Transaction(models.Model):
    issued_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='issued_to')
    issued_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='issued_by')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='transactions')
    date_issued = models.DateField()
    date_due = models.DateField(blank=True)
    date_returned = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.issued_to.first_name} {self.issued_to.last_name} - {self.book_copy.book.name}"
    
    # can expose is_overdue function
    # can expose function to calculate fine
