from .serializers import PostSerializer
from .models import Post
from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.exceptions import PermissionDenied
from UserProfile.permissions import IsOwnerOrReadOnly
class PostViewSet(generics.ListCreateAPIView):
    """
    Posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    lookup_field="id"


    def perform_update(self, serializer):
        # Only allow the owner to update the profile
        if self.request.user == serializer.instance.owner:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("You do not have permission to edit this profile.")




