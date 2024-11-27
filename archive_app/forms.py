from django import forms
from .models import Document
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = get_user_model()
        fields = ['email', 'full_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'department', 'publication_date', 'file_path', 'abstract']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 4}),
            'publication_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'max': '9999-12-31'  # Optional: Ensure the date input allows only valid dates
            }),
        }