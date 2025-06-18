# urls.py
from django.urls import path
from .views import upload_csv_view

urlpatterns = [
    path('upload/', upload_csv_view, name='upload_csv'),
]