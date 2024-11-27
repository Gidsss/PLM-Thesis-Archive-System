from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Authentication 
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),


    # Index/Home
    path('', views.index_view, name='index'),

    # Admin-specific URLs
    path('admin/manage_approvals/', views.manage_approvals, name='manage_approvals'),
    path('admin/activity_logs/', views.activity_logs, name='activity_logs'),
    path('documents/<int:pk>/edit/', views.edit_document, name='edit_document'),

    # Student-specific URLs
    path('document/list', views.document_list, name='document_list'),
    path('submit_document/', views.submit_document, name='submit_document'),
    path('documents/<int:pk>/view/', views.view_document, name='view_document'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)