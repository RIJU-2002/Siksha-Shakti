from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from .serializers import RegisterSerializer,EmailVerificationSerializer,LoginSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer,LogoutApiSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRender

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
# Create your views here.

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes=[os.environ.get('APP_SCHEME'),'http','https']

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer
    renderer_classes=(UserRender,)

    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user=User.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token
        current_sites=get_current_site(request).domain
        relativeLink=reverse('email-verify')


        
        absurl='http://'+current_sites+relativeLink+"?token="+str(token)
        email_body='Hi '+user.username+' Use link below t0 verify your email\n'+absurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class=EmailVerificationSerializer

    token_param_config=openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'Successfully Activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation link expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)


class LoginAPIview(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class=ResetPasswordEmailRequestSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        email=request.data['email']
        if User.objects.filter(email=email).exists():
                user=User.objects.get(email=email)
                uidb64=urlsafe_base64_encode(smart_bytes(user.id))
                token=PasswordResetTokenGenerator().make_token(user)
                current_sites=get_current_site(request=request).domain
                relativeLink=reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
                redirect_url=request.data.get('redirect_url','')
                absurl='http://'+current_sites+relativeLink
                email_body='Hi,\n Use link below to reset your password\n'+absurl+"?redirect_url="+redirect_url
                data={'email_body':email_body,'to_email':user.email,'email_subject':'Reset your password'}
                Util.send_email(data)
        
        return Response({'Success':'We have sent you a link to reset your password'},status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def get(self,request,uidb64,token):
        redirect_url=request.GET.get('redirect_url')
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                if len(redirect_url)>3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                
                #return Response({'error':'Token is not valid,please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
                else:
                    #return CustomRedirect(os.environ.get('FRONTEND_URL','')+'?token_valid=False')
                    return CustomRedirect(settings.FRONTEND_URL+'?token_valid=False')
            if redirect_url and len(redirect_url)>3:

            #return Response({'success':True,'message':'Credentials Valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
                return CustomRedirect(redirect_url+'?token_valid=True&?message=Credentials Valid&?uidb64='+uidb64+'&?token='+token)
            else:
                #return CustomRedirect(os.environ.get('FRONTEND_URL','')+'?token_valid=False')
                return CustomRedirect(settings.FRONTEND_URL+'?token_valid=False')

            
        except DjangoUnicodeDecodeError as identifier:
           if not PasswordResetTokenGenerator().check_token(user):
                #return Response({'error':'Token is not valid,please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
                return CustomRedirect(redirect_url+'?token_valid=False')
        
class SetNewPasswordAPIview(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self,request):
        serializer=self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Password reset success'},status=status.HTTP_200_OK)
    
class LogoutApiView(generics.GenericAPIView):
    serializer_class=LogoutApiSerializer

    permission_classes=[permissions.IsAuthenticated,]

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AuthUserAPIview(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)

    def get(self,request):
        user=User.objects.get(pk=request.user.pk)
        serializer=RegisterSerializer(user)

        return Response(serializer.data)
    
from .serializers import UserSerializer

class UserListAPIView(generics.GenericAPIView):
    serializer_class=UserSerializer
    permission_classes=(permissions.IsAuthenticated,)
    def get(self,request):
        users=User.objects.all().order_by('username')
        serializer=UserSerializer(instance=users,many=True)
        return Response(serializer.data)
    
