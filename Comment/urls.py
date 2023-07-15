from django.urls import path
from .views import CommentViewSet,CommentRetrieveUpdateDestroyView


urlpatterns = [
    path('<int:post_pk>/',CommentViewSet.as_view(),name="all_comment"),
    path('<int:post_pk>/edit/<int:pk>/',CommentRetrieveUpdateDestroyView.as_view(),name="profile_detail")
]
