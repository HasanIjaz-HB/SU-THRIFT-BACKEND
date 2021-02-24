from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from rest_framework.authtoken.views import obtain_auth_token

from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),                                      #core urlsteki urlleri alıyo
    #path('', PostView.as_view(), name='test'),
    #path('create/', PostCreateView.as_view(), name='create'),
    #path('list-create/', PostListCreateView.as_view(), name='list-create'),
    #path('productList/', ProductCreateView.as_view(), name='productList'),
    # path('userList/', UserCreateView.as_view(), name='userList'),
    path('productList/', ProductCreateView.as_view(), name='productList'),
    path('productUpdateDelete/<int:id>', ProductUpdateDelete.as_view(), name='productUpdateDelete'), #https://www.youtube.com/watch?v=E87j-Dr3kTc bu tutorial ile duzeltilecek
    path('categoryList/', categoryCreateView.as_view(), name='categoryList'),
    #path('api-auth/', include('rest_framework.urls')),
    #path('api/token/', obtain_auth_token, name='obtain-token'),
    #path('accounts/', include("allauth.urls")),
    path('home/', index, name='home'),
    #path('register/', RegistrationView.as_view(),name='register'),    canol register
    #path('dj-rest-auth/', include('dj_rest_auth.urls'))

    #path('auth/', include('rest_auth.urls')),
    #path('auth/registration/', include('rest_auth.registration.urls')),

    path('commentRates/<int:seller>', CommentUpdateDelete.as_view(), name='commentRates'),

    path('commentCreate/', CommentCreate.as_view(), name='commentCreate'),

    path('order/<int:buyer>', OrderUpdateDelete.as_view(), name='order'), 
    path('creditCard/<int:cardOwner>', CreditCardUpdateDelete.as_view(), name='creditCard'), 
    path('contact/<int:user>', ContactUpdateDelete.as_view(), name='contact'), 
    

    path('orderList/', OrderCreateView.as_view(), name='orderList'),
    path('creditCardList/', CreditCardCreateView.as_view(), name='creditCardList'),
    path('contactList/', ContactCreateView.as_view(), name='contactList'),

    path('pdf', pdf_view, name='send_file'), #DOWNLOAD API LINK FOR THE PDF.
    path('orderPdf/<int:buyer>', OrderPdf.as_view(), name='orderPdf'), 
#OrderPdf

    path('orderPdfImproved/<int:buyer>', OrderPdfImproved.as_view(), name='orderPdfImproved'), 

    path('purchases/<int:owner>', TestView.as_view(), name='test'),

    path('campaignList/', CampaignCreateView.as_view(), name='campaignList'),


]

#OrderCreateView
#OrderUpdateDelete
#CreditCardCreateView
#CreditCardUpdateDelete
#ContactCreateView
#ContactUpdateDelete