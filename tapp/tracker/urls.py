from django.urls import path 
from . import views 
from .views import edit_time_entry
from .views import create_project

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('add/', views.add_time_entry, name='add_time_entry'),
    path('edit/<int:entry_id>/', views.edit_time_entry, name='edit_time_entry'),
    path('create-project/', create_project, name='create_project'),
    path('delete/<int:entry_id>/', views.delete_time_entry, name='delete_time_entry'),

]
