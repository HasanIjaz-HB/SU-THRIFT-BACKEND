from django.db import models
#from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
# User = get_user_model()

from django.utils import timezone


#from django.contrib.auth.hashers import make_password

from authentication.models import User
class category(models.Model): #(one product can belong to multiple products. one product may have one category)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class orders(models.Model): #For having multiple products in one checkout. 
    #productInfo = models.ForeignKey(product, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_Seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    dateSold = models.DateTimeField(default=timezone.now)

class product(models.Model): # (one to many --> User may have multiple products. product cannot belong to multiple users)
    category = models.ForeignKey(category, on_delete=models.SET_NULL,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    productName = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    shortDescription = models.CharField(max_length = 150)
    longDescription = models.CharField(max_length=300)
    weight = models.IntegerField(null=True) #we can use grams to save weight. Up to 1000kg
    dateAdded = models.DateTimeField(auto_now_add=True)
    # bargain = models.BooleanField(default=False) #If seller is open for bargain
    # lastOffer = models.DecimalField(max_digits=7, decimal_places=2)
    shippingIncluded = models.BooleanField(default=False)
    imagePath = models.CharField(max_length = 200)
    currentState = models.CharField(max_length=30,default='onSale') #preparing, shipping, arrived...
    orderNum = models.ForeignKey(orders, related_name='products', on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.productName

class ratesComments(models.Model): # --> voting will be available if both voter and seller id exist in the same row in productUser table
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratesComments_Seller')
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.TextField(null=True)
    isApproved = models.BooleanField(default=False)

class campaigns(models.Model):
    campaignName = models.CharField(max_length=60)
    campaignDetails = models.TextField(null=True)
    products = models.ForeignKey(product, on_delete=models.CASCADE)
    discountAmount = models.IntegerField(null=True)
    campaignAdded = models.DateTimeField(auto_now_add=True)
    campaignEndDate = models.DateTimeField()

    def __str__(self):
        return self.campaignName

class userCreditCard(models.Model):
    cardOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    cardNum = models.CharField(max_length=19)
    expDate = models.DateField() #CharField olarak da alınabilirdi hangisi olsun? Ay Yıl gerekli gün değil çünkü
    secNum = models.CharField(max_length=3)

class contact(models.Model): #one user may have multiple contacts.
    user = models.ManyToManyField(User)
    adress = models.CharField(max_length=100)
    adress2 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=40)
    district = models.CharField(max_length=40)
    zip = models.CharField(max_length=5)
    phoneNum = models.CharField(max_length=15)
    email = models.EmailField() #User may use different emails for contact adresses
    # contactOwner = models.ForeignKey(User, on_delete=models.CASCADE)