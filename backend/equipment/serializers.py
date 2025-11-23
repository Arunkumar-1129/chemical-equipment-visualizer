from rest_framework import serializers
from .models import EquipmentDataset
import json


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    equipment_type_distribution = serializers.SerializerMethodField()
    raw_data = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature',
                  'equipment_type_distribution', 'raw_data']
    
    def get_equipment_type_distribution(self, obj):
        return obj.get_equipment_type_distribution()
    
    def get_raw_data(self, obj):
        return obj.get_raw_data()












