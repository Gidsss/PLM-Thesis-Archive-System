from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    is_active = models.BooleanField(default=True)

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