from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.FileListView.as_view(), name='file_list'),
    path('process/<int:pk>/', views.process_file, name='process_file'),
    path('extract/<int:pk>/', views.extract_message, name='extract_message'),
    path('upload-for-extraction/', views.upload_for_extraction, name='upload_for_extraction'),
    path('clear-history/', views.clear_file_history, name='clear_history'),
]
