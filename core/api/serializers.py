from rest_framework import serializers
from ..models import Product, Profile, ProductRating, CustomUser, User, VerificationCode

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'phone']

    def create(self, validated_data):
        """
        Custom create method to handle nested user creation.
        """
        user_data = validated_data.pop('user')  # Extract nested user data
        user = CustomUser.objects.create(**user_data)  # Create the user
        profile = Profile.objects.create(user=user, **validated_data)  # Create the profile
        return profile

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated):
        user = User.objects.create_user(
            username=validated['username'],
            email=validated['email'],
            password=validated['password'],
            is_active=False
        )
        # generate & email code…
        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class FarmerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'profile']

class BuyerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'profile']

class CooperativeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'profile']

class ProductSerializer(serializers.ModelSerializer):
    # owner is now represented by its primary key,
    # and will be validated against existing User queryset.
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(profile__role__in=['umuhinzi','cooperative'])
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'contact',
            'media', 'price_per_unit', 'quantity_available',
            'unit', 'owner'
        ]

class RateSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

class MarketInsightsSerializer(serializers.Serializer):
    top_products = ProductSerializer(many=True)
    top_farmers = serializers.ListField()

class ProductRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = ProductRating
        fields = ['id', 'user', 'product', 'rating']

class VerificationCodeSerializer(serializers.Serializer):
    user = UserSerializer()
    class Meta:
        model = VerificationCode
        fields = ['id','user','code','created_at','expires_at']
