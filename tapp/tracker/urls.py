from django.urls import path 
from . import views 
from .views import edit_time_entry
from .views import create_project
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('add/', views.add_time_entry, name='add_time_entry'),
    path('edit/<int:entry_id>/', views.edit_time_entry, name='edit_time_entry'),
    path('create-project/', create_project, name='create_project'),
    path('delete/<int:entry_id>/', views.delete_time_entry, name='delete_time_entry'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('employee-entry/', views.employee_entry, name='employee_entry'),
    path('employee-success/', TemplateView.as_view(template_name="tracker/employee_success.html"), name='employee_success'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]
