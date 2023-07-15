from django.urls import path
from .views import ProfileListAPIView,ProfileDetailAPIView


urlpatterns = [
    path('',ProfileListAPIView.as_view(),name="all_profile"),
    path('<str:username>/',ProfileDetailAPIView.as_view(),name="profile_detail")
]
