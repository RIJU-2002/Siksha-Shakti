from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        receiver_name = self.kwargs.get('receiver_name')
        receiver = User.objects.get(username=receiver_name)
        serializer.save(sender=self.request.user, receiver=receiver)
    

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the logged-in user
        sender = self.request.user

        # Retrieve the username of the particular user from the URL parameter
        receiver_username = self.kwargs['receiver_name']

        # Get the user object for the receiver
        receiver = User.objects.get(username=receiver_username)

        # Retrieve the messages between the sender and receiver and order them by timestamp
        queryset = Message.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        ).order_by('timestamp')

        return queryset