from django.contrib import admin
from .models import BloodRequest

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'patient_name', 'blood_group', 'city', 'required_date', 'created_at')
    list_filter = ('blood_group', 'state', 'required_date')
    search_fields = ('reference_number', 'patient_name', 'hospital_name')
    readonly_fields = ('reference_number', 'created_at')
