from django.db import models
from django.contrib.auth.models import User
import json


class EquipmentDataset(models.Model):
    """Model to store uploaded CSV datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    equipment_type_distribution = models.TextField()  # JSON string
    raw_data = models.TextField()  # JSON string of all equipment data
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def get_equipment_type_distribution(self):
        """Parse and return equipment type distribution as dict"""
        return json.loads(self.equipment_type_distribution)
    
    def get_raw_data(self):
        """Parse and return raw data as list of dicts"""
        return json.loads(self.raw_data)
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"












