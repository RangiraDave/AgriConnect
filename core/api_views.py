from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Profile, Farmer, Buyer, Cooperative, Product, ProductRating, VerificationCode
from rest_framework.views import exception_handler
from .serializers import (
    UserSerializer, ProfileSerializer, FarmerSerializer,
    BuyerSerializer, CooperativeSerializer, ProductSerializer,
    ProductRatingSerializer, VerificationCodeSerializer
)

User = get_user_model()

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
    permission_classes = [permissions.IsAuthenticated]

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.select_related('profile').all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]

class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.select_related('profile').all()
    serializer_class = BuyerSerializer
    permission_classes = [permissions.IsAuthenticated]

class CooperativeViewSet(viewsets.ModelViewSet):
    queryset = Cooperative.objects.select_related('profile').all()
    serializer_class = CooperativeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('owner').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.select_related('user','product').all()
    serializer_class = ProductRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VerificationCodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VerificationCode.objects.select_related('user').all()
    serializer_class = VerificationCodeSerializer
    permission_classes = [permissions.IsAdminUser]
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
