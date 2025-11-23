from django.contrib import admin
from .models import EquipmentDataset


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'total_count']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['filename']












