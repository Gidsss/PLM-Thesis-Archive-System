from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Index/Home
    path('', views.index_view, name='index'),

    # Admin-specific URLs
    path('admin/manage-approvals/', views.manage_approvals, name='manage_approvals'),
    path('admin/activity-logs/', views.activity_logs, name='activity_logs'),
]
