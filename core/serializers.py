from rest_framework import serializers
from .models import Province, District, Sector, Cell, Village

class RateSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'name', 'code']

class CellSerializer(serializers.ModelSerializer):
    villages = VillageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cell
        fields = ['id', 'name', 'code', 'villages']

class SectorSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True, read_only=True)
    
    class Meta:
        model = Sector
        fields = ['id', 'name', 'code', 'cells']

class DistrictSerializer(serializers.ModelSerializer):
    sectors = SectorSerializer(many=True, read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'name', 'code', 'sectors']

class ProvinceSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)
    
    class Meta:
        model = Province
        fields = ['id', 'name', 'code', 'districts'] 