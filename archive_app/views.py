from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from .forms import UserRegistrationForm, DocumentForm
from .models import Document, AuditTrail


# Initialize the custom user model
User = get_user_model()

# Index/Home
def index_view(request):
    return render(request, 'index.html')

# Authentication Views
def login_view(request):
    if request.method == 'POST':  # Check if the form is submitted via POST
        email = request.POST.get('email')  # Retrieve email from POST data
        password = request.POST.get('password')  # Retrieve password from POST data
        user = authenticate(request, email=email, password=password)  # Authenticate user
        
        if user is not None:
            login(request, user)  # Log in the user
            
            # Redirect based on user role
            if user.role == 'student':
                return redirect('document_list')  # Redirect to document list for students
            elif user.role == 'admin':
                return redirect('activity_logs')  # Redirect to activity logs for admin
            
            # Default redirect
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password. Please try again!')  # Display error message
    return render(request, 'login.html')  # Render the login page for GET or invalid POST requests

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

def profile_view(request):
    return render(request, 'profile.html')

# Document List & Search (All Roles)
def document_list(request):
    query = request.GET.get('q')  # For search functionality
    status_filter = request.GET.get('status')  # For status filtering (Pending, Approved)


     # Display all documents
    documents = Document.objects.all()

    # Apply search query filter
    if query:
        documents = documents.filter(
            title__icontains=query
        )  # Add additional filters like keywords, abstract, etc., if needed.

    # Apply status filter
    if status_filter:
        documents = documents.filter(status=status_filter)

    # Paginate documents
    paginator = Paginator(documents, 10)  # Show 10 documents per page
    page = request.GET.get('page')
    documents = paginator.get_page(page)

    # Get unique departments for dropdown (if needed for other filters)
    departments = Document.objects.values_list('department', flat=True).distinct()

    return render(request, 'document_list.html', {
        'documents': documents,
        'departments': departments,
        'selected_status': status_filter,  # Pass the selected status to the template
        'query': query,  # Pass the search query to the template
    })

# Document Upload (Students)
@login_required
def submit_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user  # Link the user who uploaded the document
            document.save()
            return redirect('document_list')  # Redirect to the document list after submission
    else:
        form = DocumentForm()
    return render(request, 'document_list.html', {'form': form})
    
# Document View (All Roles)
def view_document(request, pk):
    document = get_object_or_404(Document, pk=pk)

    return render(request, 'view_document.html', {'document': document})

# Document Edit (Admin Only)
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk)

    # Restrict access to admins only
    if not request.user.is_authenticated or not request.user.role == 'admin':
        return HttpResponseForbidden("You do not have permission to edit this document.")

    if request.method == "POST":
        # Handle form submission for updating document
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')  # Redirect back to document list
    else:
        form = DocumentForm(instance=document)

    return render(request, 'admin/edit_document.html', {'form': form, 'document': document})

# Document Approvals (Admin Only)
@permission_required('archive_app.can_approve_documents', raise_exception=True)
def manage_approvals(request):
    pending_documents = Document.objects.filter(status="Pending")
    modal_message = None  # Variable to hold the message to be displayed in the modal
    modal_status = None   # Variable to determine if the modal should show success or failure

    if request.method == "POST":
        action = request.POST.get('action')
        doc_id = request.POST.get('doc_id')

        try:
            document = get_object_or_404(Document, id=doc_id)

            if action == "approve":
                document.status = "Approved"
                modal_message = f"Document '{document.title}' approved successfully."
                modal_status = "success"
            elif action == "reject":
                document.status = "Rejected"
                modal_message = f"Document '{document.title}' rejected successfully."
                modal_status = "success"
            else:
                modal_message = "Invalid action."
                modal_status = "error"

            document.save()

            # Log the approval/rejection in AuditTrail
            AuditTrail.objects.create(
                user=request.user,
                action=f"{action.capitalize()} Document: {document.title}",
            )

        except Exception as e:
            modal_message = f"An error occurred: {str(e)}"
            modal_status = "error"

    return render(request, 'admin/manage_approvals.html', {
        'pending_documents': pending_documents,
        'modal_message': modal_message,
        'modal_status': modal_status,
    })


# Activity Logs (Admin Only)
@permission_required('archive_app.can_view_logs', raise_exception=True)
def activity_logs(request):
    logs = AuditTrail.objects.all().order_by('-timestamp')
    paginator = Paginator(logs, 20)  # Paginate logs
    page = request.GET.get('page')
    logs = paginator.get_page(page)
    return render(request, 'admin/activity_logs.html', {'logs': logs})