from .models import UserProfile
from authentication.models import User
#from . permissions import IsOwnerOrReadOnly
from . serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


from rest_framework import generics, permissions
#from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.exceptions import PermissionDenied,NotFound

"""def my_function(image_file_path):
    url = 'http://your-api-endpoint/mymodels/'
    files = {'image': open(image_file_path, 'rb')}
    response = requests.post(url, files=files)
    
    if response.status_code == 201:  # Assuming successful creation (HTTP status code 201)
        return "Image uploaded successfully."
    else:
        return "Error uploading the image."""

class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
            return self.queryset.get(owner=user)
        except Exception as e:
            raise NotFound("The userprofile is not found or created")


    def perform_update(self, serializer):
        # Only allow the owner to update the profile
        if self.request.user == serializer.instance.owner:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("You do not have permission to edit this profile.")

class ProfileListAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #need to add get_query set to make the searc acc to loaction

    

