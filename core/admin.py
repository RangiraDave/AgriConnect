# admin.py
from django.contrib import admin
from .models import CustomUser
from django.contrib import admin
from .models import CustomUser, Profile, Farmer, Buyer, Cooperative, Product, Province, District, Sector, Cell, Village
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


# User = get_user_model()

# user = User.objects.get(username='dave')
# print(f"User: {user.username}, Role: {user.profile.role}")


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
    list_display = ('profile', 'province', 'district', 'sector', 'cell', 'village')
    list_filter = ('province', 'district', 'sector')
    search_fields = ('profile__user__username', 'specific_location')


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
    list_display = ('name', 'owner', 'created_at', 'price_per_unit', 'quantity_available')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'owner__username')
    ordering = ('-created_at',)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'province')
    list_filter = ('province',)
    search_fields = ('name', 'code')
    ordering = ('province', 'name')


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'district', 'province')
    list_filter = ('district__province', 'district')
    search_fields = ('name', 'code')
    ordering = ('district', 'name')

    def province(self, obj):
        return obj.district.province.name
    province.short_description = 'Province'


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sector', 'district', 'province')
    list_filter = ('sector__district__province', 'sector__district', 'sector')
    search_fields = ('name', 'code')
    ordering = ('sector', 'name')

    def district(self, obj):
        return obj.sector.district.name
    district.short_description = 'District'

    def province(self, obj):
        return obj.sector.district.province.name
    province.short_description = 'Province'


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'cell', 'sector', 'district', 'province')
    list_filter = ('cell__sector__district__province', 'cell__sector__district', 'cell__sector', 'cell')
    search_fields = ('name', 'code')
    ordering = ('cell', 'name')

    def sector(self, obj):
        return obj.cell.sector.name
    sector.short_description = 'Sector'

    def district(self, obj):
        return obj.cell.sector.district.name
    district.short_description = 'District'

    def province(self, obj):
        return obj.cell.sector.district.province.name
    province.short_description = 'Province'

# Example data for Rwanda provinces
PROVINCES = [
    {'name': 'Kigali City', 'code': '01'},
    {'name': 'Southern Province', 'code': '02'},
    {'name': 'Western Province', 'code': '03'},
    {'name': 'Northern Province', 'code': '04'},
    {'name': 'Eastern Province', 'code': '05'},
]
