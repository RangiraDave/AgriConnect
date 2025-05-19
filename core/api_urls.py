from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    ProvinceViewSet, DistrictViewSet,
    SectorViewSet, CellViewSet, VillageViewSet
)

router = DefaultRouter()
router.register(r'provinces', ProvinceViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'cells', CellViewSet)
router.register(r'villages', VillageViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 