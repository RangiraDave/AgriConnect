from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Province, District, Sector, Cell, Village
from .serializers import (
    ProvinceSerializer, DistrictSerializer,
    SectorSerializer, CellSerializer, VillageSerializer
)

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['get'])
    def districts(self, request, pk=None):
        province = self.get_object()
        districts = District.objects.filter(province=province)
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = District.objects.all()
        province_id = self.request.query_params.get('province', None)
        if province_id is not None:
            queryset = queryset.filter(province_id=province_id)
        return queryset

    @action(detail=True, methods=['get'])
    def sectors(self, request, pk=None):
        district = self.get_object()
        sectors = Sector.objects.filter(district=district)
        serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data)

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Sector.objects.all()
        district_id = self.request.query_params.get('district', None)
        if district_id is not None:
            queryset = queryset.filter(district_id=district_id)
        return queryset

    @action(detail=True, methods=['get'])
    def cells(self, request, pk=None):
        sector = self.get_object()
        cells = Cell.objects.filter(sector=sector)
        serializer = CellSerializer(cells, many=True)
        return Response(serializer.data)

class CellViewSet(viewsets.ModelViewSet):
    queryset = Cell.objects.all()
    serializer_class = CellSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Cell.objects.all()
        sector_id = self.request.query_params.get('sector', None)
        if sector_id is not None:
            queryset = queryset.filter(sector_id=sector_id)
        return queryset

    @action(detail=True, methods=['get'])
    def villages(self, request, pk=None):
        cell = self.get_object()
        villages = Village.objects.filter(cell=cell)
        serializer = VillageSerializer(villages, many=True)
        return Response(serializer.data)

class VillageViewSet(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Village.objects.all()
        cell_id = self.request.query_params.get('cell', None)
        if cell_id is not None:
            queryset = queryset.filter(cell_id=cell_id)
        return queryset 