from django.urls import path
from .views import PostViewSet,PostDetailView


urlpatterns = [
    path('',PostViewSet.as_view(),name="all_post"),
    path('<int:id>/',PostDetailView.as_view(),name="profile_detail")
]
