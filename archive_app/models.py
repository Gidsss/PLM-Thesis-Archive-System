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
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    publication_date = models.DateField()
    document_type = models.CharField(max_length=100)
    degree_name = models.CharField(max_length=100)
    subject_categories = models.CharField(max_length=255)
    college = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    advisor = models.CharField(max_length=100)
    panel_members = models.TextField()
    keywords = models.TextField()
    language = models.CharField(max_length=50)
    file_path = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

# Audit Trail Model
class AuditTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)