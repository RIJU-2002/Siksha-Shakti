from .models import Comment
from Post.models import Post
from rest_framework import permissions,generics
from django.shortcuts import get_object_or_404
from UserProfile.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied

from . serializers import CommentSerializer


# Create your views here.
class CommentViewSet(generics.ListCreateAPIView):
    """Comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    #lookup_field="post"
    """def get_object(self):
        post_id=self.kwargs(["post_id"])
        return Comment.objects.filter(post=post_id)"""

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = generics.get_object_or_404(Post, id=post_pk)
        serializer.save(post=post, author=self.request.user)
    
    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post=post_pk)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post=post_pk)
    
    def get_object(self):
        post_pk = self.kwargs.get('post_pk')
        comment_pk = self.kwargs.get('pk')
        queryset = self.get_queryset()
        return get_object_or_404(queryset, post=post_pk, id=comment_pk)