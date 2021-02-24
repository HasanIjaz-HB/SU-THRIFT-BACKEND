from django.contrib import auth

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import  *


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = (
            'id',
            'productName',
            'owner',
            'category',
            'price',
            'dateAdded',
            'owner',
            'shortDescription',
            'longDescription',
            'imagePath',
            'orderNum',
        )

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = (
            'name', 
            'description',
        )

class commentRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ratesComments
        fields = (
            'seller',
            'voter',
            'rate',
            'comment',
          #  'isApproved' this will be added in 4th sprint
        )

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = (
            'name', 
            'description',
        )

class campaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = campaigns
        fields = (
            'campaignName', 
            'campaignDetails',
            'products',
            'discountAmount',
            'campaignAdded',
            'campaignEndDate',
        )

class ordersSerializer(serializers.ModelSerializer):
    products = productSerializer(many=True, read_only=True)
    
    class Meta:
        model = orders
        fields = (
            'id',
            'products', 
            'seller',
            'buyer',
            'dateSold',
        )


"""
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'tenure')

class ClassroomSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(source='teacher_set')

    class Meta:
        model = Classroom
"""

class creditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = userCreditCard 
        fields = (
            'cardOwner', 
            'cardNum',
            'expDate',
            'secNum',
        )

class contactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact
        fields = (
            'user',
            'adress', 
            'adress2',
            'city',
            'district',
            'zip',
            'phoneNum',
            'email',
            'contactOwner',
        )