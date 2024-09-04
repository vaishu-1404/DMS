from django.contrib import admin
from django.urls import path, include
from api.views import *

urlpatterns = [
    # path('create-client', view=create_client, name='create-client')
    # path('upload', view=upload, name='upload')
    # path('handle/', ClientViewSet.as_view({'get': 'list', 'post': 'create'}), name="handle"),
    path('create-client',view=create_client, name='create-client'),
    path('delete-client/<int:pk>',view=delete_client, name='delete-client'),
    path('list-client',view=list_client, name='list-client'),
]
