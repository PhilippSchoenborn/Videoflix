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
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('verify-email/<str:token>/', verify_email_view, name='verify_email'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
