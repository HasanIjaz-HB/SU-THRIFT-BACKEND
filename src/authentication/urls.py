from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView, LogoutAPIView, UserList, ChangePasswordView, User
#PasswordTokenCheckAPI, SetNewPasswordAPIView RequestPasswordResetEmail
from .views import MyObtainTokenPairView, UpdateProfileView, TokenObtainPairView,LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
     path('register', RegisterView.as_view(), name="register"),
     path('email-verify', VerifyEmail.as_view(), name="email-verify"),
     #path('login', LoginAPIView.as_view(), name="login"),
     #path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     #path('logout', LogoutAPIView.as_view(), name="logout"),
     path('logout/', LogoutView.as_view(), name='auth_logout'),

     #path('request-reset-email', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
     #path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
     #path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
     path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
     path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
     path('userList', UserList.as_view(), name="userList"),
     path('user/<int:pk>/', User.as_view(), name="userList"),

]