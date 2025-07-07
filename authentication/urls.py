"""
URL configuration for authentication app
"""
from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    user_logout_view,
    verify_email_view,
    PasswordResetRequestView,
    PasswordResetView,
    UserProfileView
)

app_name = 'authentication'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', user_logout_view, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', verify_email_view, name='activate'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_confirm/<str:uidb64>/<str:token>/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
