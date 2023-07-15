from .models import UserProfile
from rest_framework import serializers
from authentication.models import User 
from .models import UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    profile_image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
