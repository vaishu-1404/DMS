from django.contrib import admin
from django.urls import path, include
from api.views import *

urlpatterns = [
    path('create-client', create_client.as_view(), name='create-client'),
    path('edit-client/<int:pk>',view=edit_client, name='edit-client'),
    path('delete-client/<int:pk>',view=delete_client, name='delete-client'),
    path('list-client',view=list_client, name='list-client'),
]
