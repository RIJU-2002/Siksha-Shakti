from django.urls import path
from .views import RegisterView,VerifyEmail,LoginAPIview,PasswordTokenCheckAPI,RequestPasswordResetEmail,SetNewPasswordAPIview,LogoutApiView,AuthUserAPIview,UserListAPIView
from rest_framework_simplejwt.views import (TokenRefreshView)
from . import views

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginAPIview.as_view(),name="login"),
    path('logout/',LogoutApiView.as_view(),name="logout"),
    path('user/',AuthUserAPIview.as_view(),name='user'),
    path('email-verify/',VerifyEmail.as_view(),name="email-verify"),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('request-reset-email',RequestPasswordResetEmail.as_view(),name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password-reset-confirm'),
    path('password-reset-complete/',SetNewPasswordAPIview.as_view(),name='password-reset-complete'),
    path('user_list/', UserListAPIView.as_view(), name='user_list')
]
