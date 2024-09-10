from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('create-client', create_client.as_view(), name='create-client'),
    path('edit-client/<int:pk>',view=edit_client, name='edit-client'),
    path('delete-client/<int:pk>',view=delete_client, name='delete-client'),
    path('list-client',view=list_client, name='list-client'),
    path('detail-client/<int:pk>', view=detail_client, name='detail-client'),

    path('create-bank/<int:pk>', view=create_bank, name='create-bank'),
    path('edit-bank/<int:pk>/<int:bank_pk>',view=edit_bank, name='edit-bank'),
    path('list-bank/<int:pk>',view=list_bank, name='list-bank'),
    path('delete-bank/<int:pk>/<int:bank_pk>', view=delete_bank, name='delete-bank'),

    path('create-owner/<int:pk>',view=create_owner, name='create-owner'),
    path('edit-owner/<int:pk>/<int:owner_pk>',view=edit_owner, name='edit-owner'),
    path('list-owner/<int:pk>',view=list_owner, name='list-owner'),
    path('delete-owner/<int:pk>/<int:owner_pk>',view=delete_owner, name='delete-owner'),

    path('user-login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users', view=getUsers, name='users'),
    path('user-profile', view=getUserProfile, name='user-profile'),
    path('user-dashboardform', view=dashboarduser, name='dashboard-user'),
    path('user-clientform/<int:pk>', view=clientuser, name='client'),
    path('activate/<uidb64>/<token>',ActivateAccountView.as_view(),name='activate'),
    path('edit-clientuser/<int:pk>/<int:user_pk>', view=edit_clientuser, name='edit-clientuser'),
    path('user-dashboarduser/<int:user_pk>', view=edit_dashboardUser, name='edit-dashboarduser'),
    path('delete-clientuser/<int:pk>/<int:user_pk>', view=delete_clientuser, name='delete-clientuser'),
    path('delete-dashboarduser/<int:user_pk>', view=delete_dashboarduser, name='delete-dashboarduser'),

    path('create-companydoc/<int:pk>', view=create_companydoc, name='create-companydoc'),
    path('edit-companydoc/<int:pk>/<int:companydoc_pk>', view=edit_companydoc, name='edit-companydoc'),
    path('list-companydoc/<int:pk>', view=list_companydoc, name='list-companydoc'),
    path('delete-companydoc/<int:pk>/<int:companydoc_pk>', view=delete_companydoc, name='delete-companydoc'),

]
