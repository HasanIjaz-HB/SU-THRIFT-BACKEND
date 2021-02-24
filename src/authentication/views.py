from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import permissions

from rest_framework.permissions import IsAuthenticated,AllowAny #Others important to consider --> IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer,  RegisterSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from .serializers import LogoutSerializer, MyTokenObtainPairSerializer,ChangePasswordSerializer, UpdateUserSerializer
from .models import User
from .utils import Util

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

import jwt

class UserCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all() 

#class RegistrationView(generics.CreateAPIView):
#   serializer_class = RegistrationSerializer

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        #Preparing email and its content
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = '127.0.0.1:8000'
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):

    permission_classes = (AllowAny,)

    def get(self,request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])

            if not user.emailConf:
                user.emailConf=True
                user.save()

            return Response({'email' : 'Successfully activated'}, status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error' : 'Activation link expired'}, status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error' : 'Invalid token'}, status.HTTP_400_BAD_REQUEST)

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class= LogoutSerializer

    #Only Authanticated user which has refresh token can access this api
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    
class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

# class RequestPasswordResetEmail(generics.GenericAPIView):

#     serializer_class = ResetPasswordEmailRequestSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)

#         email = request.data.get('email', '')

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(
#                 request=request).domain
#             relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

#             redirect_url = request.data.get('redirect_url', '')
#             absurl = 'http://'+current_site + relativeLink
#             email_body = 'Hello, \n Use link below to reset your password  \n' + \
#                 absurl+"?redirect_url="+redirect_url
#             data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Reset your passsword'}
#             Util.send_email(data)
#             return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
#         if not User.objects.filter(email=email).exists():
#                 return Response ({'error' : 'Invalid email adress'}, status=status.HTTP_400_BAD_REQUEST)



# class PasswordTokenCheckAPI(generics.GenericAPIView):

#     def get(self,request,uidb64,token):
#         print('selam genc')
#         try:
#             id=smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response ({'error':'Token is not valid, plese request a new one'},status=status.HTTP_401_UNAUTHORIZED)

#             return Response ({'success':True,'message':'Credentials Valid','u,db64': uidb64,'token':token},status=status.HTTP_200_OK)

            
#         except Exception as e:
#             print(e)
#             if not PasswordResetTokenGenerator().check_token(user):
#                 return Response ({'error':'Token is not valid, plese request a new one'},status=status.HTTP_401_UNAUTHORIZED)



# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def patch(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all() 

class User(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all() 

@login_required
def index(request):
    return render(request, 'homePage.html')