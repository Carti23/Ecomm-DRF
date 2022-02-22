from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from knox.auth import AuthToken
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
import stripe
# Create your views here.


def serialize_user(user):
    return {
        "usernme": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }



"""Register API"""
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user_info": serialize_user(user),
            "token": token
        })

""" User API """
class UserListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

""" Create a user """
class UserCreateApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

""" User Detail """
class UserDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

""" Authentication System """
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


""" Category API """
class CategoryListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


""" Create a category """
class CategoryCreateApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

""" Product API """
class ProductListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


""" Create a Product """
class ProductCreateApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

""" Details about product """

class ProductDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

""" Cart Api """
# class CartApi(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAnAuthor, )
#     serializer_class = CartSerilizer
#     queryset = Cart.objects.all()



stripe.api_key = settings.STRIPE_SECRET_KEY

""" Payment system """

class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'prod_LCRUvoyecftadd',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )

            return redirect(checkout_session.url)
        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )