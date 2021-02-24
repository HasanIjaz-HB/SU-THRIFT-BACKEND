import jwt

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse

from rest_framework.permissions import IsAuthenticated #Others important to consider --> IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from .serializers import *
from core.models import *
from authentication.models import *
from authentication.utils import Util
# from authentication.serializers import UserSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def pdf_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


class ProductCreateView(generics.ListCreateAPIView):
    serializer_class = productSerializer
    queryset = product.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category__name', 'productName']
    #ordering_fields = ['productName', 'category__name','price'] #it can order by anything if we don't specify fields
    #http://127.0.0.1:8000/productList/?ordering=price #normal order
    #http://127.0.0.1:8000/productList/?ordering=-price #reverse order

    #http://127.0.0.1:8000/productList/?search=Mutfak
    #http://127.0.0.1:8000/productList/?search=asdf
    #if searching with foreign key, use foreignKeyName__attributeNameFromTableOfTheForeignKey

# class UserCreateView(generics.ListCreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all() 

class categoryCreateView(generics.ListCreateAPIView):
    serializer_class = categorySerializer
    queryset = category.objects.all() 

class ProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = productSerializer
    queryset = product.objects.all()
    lookup_field = 'id'

class CommentUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = commentRateSerializer
    queryset = ratesComments.objects.all()
    lookup_field = 'seller'

class CommentCreate(generics.ListCreateAPIView):
    serializer_class = commentRateSerializer
    queryset = ratesComments.objects.all()
# serializer_class = ordersSerializer
# queryset = orders.objects.all()
# lookup_field = 'buyer'

# def retrieve(self, request, *args, **kwargs):
# instance = self.get_object()
# serializer = self.get_serializer(instance)
    def create(self, request, *args, **kwargs):
        print('I\'m in comment creation API')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print('In create func')
        data = serializer.validated_data

        totalComments = 0
        if (ratesComments.objects.filter(seller=data['seller']).exists()):
            totalComments = ratesComments.objects.filter(seller=data['seller']).count()
            #totalComments = r.entry_set.count()
        
        user = User.objects.get(email=data['seller'])
        preAverage = 0
        if (user.averageRate != None):
            preAverage = user.averageRate
        user.averageRate = ((preAverage * totalComments) + data['rate']) / (totalComments + 1)
        user.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrderCreateView(generics.ListCreateAPIView):
    serializer_class = ordersSerializer
    queryset = orders.objects.all() 

class OrderUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ordersSerializer
    queryset = orders.objects.all()
    lookup_field = 'buyer'

class CreditCardCreateView(generics.ListCreateAPIView):
    serializer_class = creditCardSerializer
    queryset = userCreditCard.objects.all() 

class CreditCardUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = creditCardSerializer
    queryset = userCreditCard.objects.all()
    lookup_field = 'cardOwner'

class ContactCreateView(generics.ListCreateAPIView):
    serializer_class = contactInfoSerializer
    queryset = contact.objects.all() 

class ContactUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = contactInfoSerializer
    queryset = contact.objects.all()
    lookup_field = 'user'

class CampaignCreateView(generics.ListCreateAPIView):
    serializer_class = campaignSerializer
    queryset = campaigns.objects.all() 

class OrderPdf(generics.RetrieveAPIView):
    serializer_class = ordersSerializer
    queryset = orders.objects.all()
    lookup_field = 'buyer'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        ########## DATA MANIPULATION #########
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        name = data['buyer']
        p.drawString(100, 100, str(name))

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
        ######################################
        # return Response(data)

class OrderPdfImproved(generics.RetrieveAPIView):
    serializer_class = ordersSerializer
    queryset = orders.objects.all()
    lookup_field = 'buyer'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        ########## DATA MANIPULATION #########
        #page size 595.27,841.89
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        #Title
        orderNum = str(17*data['id'])
        p.setFont("Helvetica", 20)
        p.setFillColorRGB(0,0,1)
        p.setStrokeColorRGB(0.2,0.5,0.3)
        p.drawString(170, 800, ("Sabanci Thrift Shop Invoice #" + orderNum ))#Multiplied with 17 so users won't know their actual id's
        
        p.setFont("Helvetica", 14)
        p.setFillColorRGB(0,0,0)
        p.setStrokeColorRGB(0.2,0.5,0.3)

        yVal = 720

        buyerInfo = User.objects.get(id=data['buyer']) #get the user info with buyer's id
        buyerName = buyerInfo.first_name + " " + buyerInfo.last_name

        p.drawString(100, 740, ("Buyer Name: " + str(buyerName)))

        #buyer = str(data['buyer'])
        #p.drawString(100, yVal, buyer)
        #yVal -= 20
        totalPrice = 0.0

        dateSold = str(data['dateSold'])
        p.drawString(100, yVal, dateSold)
        for prod in data['products']:
            productName = str(prod['productName'])
            yVal -= 40
            p.drawString(100, yVal, productName)
            yVal -= 20

            ownerInfo = User.objects.get(id=prod['owner']) #get the user info with buyer's id
            ownerName = ownerInfo.first_name + " " + ownerInfo.last_name

            #owner = str(prod['owner'])
            p.drawString(100, yVal, ("Owner: " + ownerName))
            yVal -= 20

            totalPrice += float(prod['price'])
            price = str(prod['price'])
            p.drawString(100, yVal, price)

        p.drawString(400, 60, ("Total Price: " + str(totalPrice)))        

        #Draw Lines
        p.line(50,800,50,50)
        p.line(545,800,545,50)
       
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        email_data={'email_body':p,'to_email':user.email,'email_subject': 'Order invoice','attachment':p}
        Util.attachement_email(email_data)
        return FileResponse(buffer, as_attachment=True, filename='Invoice.pdf')
        ######################################
        # return Response(data)

class TestView(APIView):

    #permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        querySet = productSerializer.objects.all()
        serializer = productSerializer(querySet, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = productSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)




@login_required
def index(request):
    return render(request, 'homePage.html')