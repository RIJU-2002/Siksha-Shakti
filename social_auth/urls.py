from django.urls import path
from .views import GoggleSocialAuthView,FacebookSocialAuthView

urlpatterns = [
    path('google/',GoggleSocialAuthView.as_view(),name='google'),
    path('facebook/',FacebookSocialAuthView.as_view(),name='facebook'),
]
