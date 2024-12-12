from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Explicitly set the role to 'admin'

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
# User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    username = None  # Remove the username field
    first_name = None  # Remove the first_name field
    last_name = None  # Remove the last_name field

    email = models.EmailField(unique=True)  # Use email as the unique identifier
    full_name = models.CharField(max_length=255, blank=True)  # Custom full_name field
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()  # Attach the custom manager
    USERNAME_FIELD = 'email'  # Set email as the unique identifier for authentication
    REQUIRED_FIELDS = []  # Remove the requirement for other fields during user creation

    def is_student(self):
        return self.role == 'student'
    
# Document Model
class Document(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    ]
    title = models.CharField(max_length=255)  # Required
    abstract = models.TextField(blank=True, null=True)  # Optional
    publication_date = models.DateField(blank=True, null=True)
    document_type = models.CharField(max_length=100, blank=True, null=True)  # Optional
    degree_name = models.CharField(max_length=100, blank=True, null=True)  # Optional
    subject_categories = models.CharField(max_length=255, blank=True, null=True)  # Optional
    college = models.CharField(max_length=100, blank=True, null=True)  # Optional
    department = models.CharField(max_length=100)  # Required
    advisor = models.CharField(max_length=100, blank=True, null=True)  # Optional
    panel_members = models.TextField(blank=True, null=True)  # Optional
    keywords = models.TextField(blank=True, null=True)  # Optional
    language = models.CharField(max_length=50, blank=True, null=True)  # Optional
    file_path = models.FileField(upload_to='documents/')  # Required
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Required
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Required

# Audit Trail Model
class AuditTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)