from rest_framework import serializers
from . import google,facebook
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class GoggleSocialAuthSerializer(serializers.Serializer):
    auth_token=serializers.CharField()

    def validate_auth_tokens(self,auth_token):
        user_data=google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('The token is invalid or expired.Please login again')
        
        if user_data['aud']!=os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('opps,who are you?.')
        
        user_id=user_data['sub']
        email=user_data['email']
        name=user_data['name']
        provider='google'

        return register_social_user(provider=provider,user_id=user_id,email=email,name=name)

class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_tokens=serializers.CharField()
    def validate_auth_tokens(self,auth_token):
        user_data=facebook.Facebook.validate(auth_token)
        print(user_data)
        try:
            user_id=user_data['id']
            email=user_data['email']
            name=user_data['name']
            provider='facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception as identifiers:
            print(identifiers)
            raise serializers.ValidationError(
                'The token is invalid or expired.Please login again.'
            )