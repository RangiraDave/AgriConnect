from django.contrib import admin
from .models import CustomUser
from django.contrib import admin
from .models import CustomUser, Profile, Farmer, Buyer, Cooperative, Product
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')

class CustomUserAdmin(UserAdmin):
    """
    Customizing the User admin interface
    """
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_verified', 'email_verified', 'is_staff')
    list_filter = ('role', 'is_verified', 'email_verified', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'is_verified', 'email_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Verification', {'fields': ('verification_code',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_verified', 'email_verified')}
         ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Customizing the Profile admin interface
    """
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email')


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    """
    Customizing the Farmer admin interface
    """
    list_display = ('profile', 'location')
    search_fields = ('profile__user__username', 'location')


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    """
    Customizing the Buyer admin interface
    """
    list_display = ('profile',)
    search_fields = ('profile__user__username',)


@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    """
    Customizing the Cooperative admin interface
    """
    list_display = ('profile',)
    search_fields = ('profile__user__username',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Customizing the Product admin interface
    """
    list_display = ('name', 'owner', 'location', 'created_at')
    list_filter = ('location', 'created_at', 'updated_at')
    search_fields = ('name', 'owner__username', 'location')
    ordering = ('-created_at',)
