from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/', UserListApi.as_view(), name='all-users'),
    path('users-create/', UserCreateApi.as_view(), name='create-users'),
    path('create-checkout-session/', StripeCheckoutView.as_view()),
    path('category-create/', CategoryCreateApi.as_view(), name='create-category'),
    path('users/<int:pk>/', UserDetailApi.as_view(), name='detail-users'),
    path('register/', register, name='register-users'),
    path('category/', CategoryListApi.as_view(), name='register-users'),
    path('products/', ProductListApi.as_view(), name='all-products'),
    path('products-create/', ProductCreateApi.as_view(), name='create-products'),
    path('product/<int:pk>/', ProductDetailApi.as_view(), name='detail-products'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
