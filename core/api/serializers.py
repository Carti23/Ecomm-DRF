from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

""" User Serializer """
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',  'first_name', 'last_name', 'username')


""" Category Serializer """
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


""" Regiater Serializer """
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


""" Product Serializer """
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# """ Cart Serailzier """
# class CartSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = '__all__'