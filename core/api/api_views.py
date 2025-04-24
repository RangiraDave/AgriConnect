from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import get_user_model
from ..models import Profile, Farmer, Buyer, Cooperative, Product, ProductRating, VerificationCode
from django.db import models
from rest_framework.views import exception_handler
from .serializers import (
    MarketInsightsSerializer, SignupSerializer, UserSerializer, ProfileSerializer, FarmerSerializer,
    BuyerSerializer, CooperativeSerializer, ProductSerializer,
    ProductRatingSerializer, VerificationCodeSerializer, VerifyEmailSerializer
)

User = get_user_model()

# Auth endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    ser = SignupSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    user = ser.save()
    # send email code…
    return Response({'detail':'Verification code sent.'}, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    ser = VerifyEmailSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    # lookup code, activate user…
    return Response({'detail':'Email verified.'})

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # use SimpleJWT’s TokenObtainPairView or manual authenticate + RefreshToken
    from rest_framework_simplejwt.views import TokenObtainPairView
    return TokenObtainPairView.as_view()(request._request)

# Profile
@api_view(['GET','PUT'])
def profile(request):
    prof = request.user.profile
    if request.method=='GET':
        return Response(ProfileSerializer(prof).data)
    ser = ProfileSerializer(prof, data=request.data, partial=True)
    ser.is_valid(raise_exception=True)
    ser.save()
    return Response(ser.data)

# Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('owner').all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def rate(self, request, pk=None):
        product = self.get_object()
        ser = RateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rating, _ = ProductRating.objects.update_or_create(
            product=product, user=request.user,
            defaults={'rating': ser.validated_data['rating']}
        )
        # notify owner via Channels…
        return Response({'detail':'Rated.'})

# Market insights
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access
def market_insights(request):
    top_products = Product.objects.annotate(
        avg_rating=models.Avg('ratings__rating')
    ).order_by('-avg_rating')[:5]
    # build top_farmers similarly…
    data = MarketInsightsSerializer({
        'top_products': top_products,
        'top_farmers': []
    }).data
    return Response(data)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    return response

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(role='umuhinzi')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(role='umuguzi')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CooperativeViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(role='cooperative')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('owner').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.select_related('user','product').all()
    serializer_class = ProductRatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VerificationCodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VerificationCode.objects.select_related('user').all()
    serializer_class = VerificationCodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
