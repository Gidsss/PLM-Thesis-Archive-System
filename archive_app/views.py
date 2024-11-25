from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import UserRegistrationForm, DocumentUploadForm
from .models import Document, AuditTrail

# Initialize the custom user model
User = get_user_model()

# Index/Home
def index_view(request):
    return render(request, 'index.html')

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to a homepage (create it later)
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            full_name = form.cleaned_data['full_name']

            # Create the user
            user = User.objects.create_user(
                email=email,
                password=password,
                role='student',  # Automatically set role to "student"
                full_name=full_name
            )
            user.save()

            messages.success(request, 'Registration successful. Please log in.')
            
             # Render the same page to allow for delay
            return render(request, 'register.html', {'form': form, 'redirect': True})
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Document List & Search (All Roles)
def document_list(request):
    query = request.GET.get('q')  # For search functionality
    documents = Document.objects.filter(status="Approved")  # Only approved documents

    if query:
        documents = documents.filter(
            title__icontains=query
        )  # Add filters for title, keywords, etc.

    paginator = Paginator(documents, 10)  # Paginate documents
    page = request.GET.get('page')
    documents = paginator.get_page(page)

    return render(request, 'document_list.html', {'documents': documents})

# Document Upload (Students)
@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.status = "Pending"  # Default to pending for approval
            document.save()
            # Log the action in AuditTrail
            AuditTrail.objects.create(
                user=request.user,
                action="Uploaded Document",
                timestamp=document.created_at
            )
            return redirect('document_list')  # Redirect to document list
    else:
        form = DocumentUploadForm()
    return render(request, 'upload_document.html', {'form': form})

# Document Approvals (Admin Only)
@permission_required('archive_app.can_approve_documents', raise_exception=True)
def manage_approvals(request):
    pending_documents = Document.objects.filter(status="Pending")
    if request.method == "POST":
        doc_id = request.POST.get('doc_id')
        action = request.POST.get('action')
        document = get_object_or_404(Document, id=doc_id)

        if action == "approve":
            document.status = "Approved"
        elif action == "reject":
            document.status = "Rejected"

        document.save()
        # Log the approval/rejection in AuditTrail
        AuditTrail.objects.create(
            user=request.user,
            action=f"{action.capitalize()} Document: {document.title}",
            timestamp=document.updated_at
        )
        return JsonResponse({'status': 'success'})  # AJAX response

    return render(request, 'admin/manage_approvals.html', {'pending_documents': pending_documents})

# Activity Logs (Admin Only)
@permission_required('archive_app.can_view_logs', raise_exception=True)
def activity_logs(request):
    logs = AuditTrail.objects.all().order_by('-timestamp')
    paginator = Paginator(logs, 20)  # Paginate logs
    page = request.GET.get('page')
    logs = paginator.get_page(page)
    return render(request, 'admin/activity_logs.html', {'logs': logs})