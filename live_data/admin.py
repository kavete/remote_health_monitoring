from django.contrib import admin

# Register your models here.
from .models import Ward, Patient, Microcontroller, WardReading, PatientVitalReading

class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location')
    search_fields = ('name', 'description') 

admin.site.register(Ward, WardAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward', 'bed_number', 'age', 'weight', 'height')
    search_fields = ('name', 'ward__name', 'bed_number')
    list_filter = ('ward', 'age')

admin.site.register(Patient, PatientAdmin)

class PatientVitalReadingAdmin(admin.ModelAdmin):
    list_display = ('microcontroller', 'timestamp')
    search_fields = ('microcontroller__identifier',)

admin.site.register(PatientVitalReading, PatientVitalReadingAdmin)

class MicrocontrollerAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'patient', 'installed_on')
    search_fields = ('name', 'identifier',)
    

admin.site.register(Microcontroller,MicrocontrollerAdmin)

class WardReadingAdmin(admin.ModelAdmin):
    list_display = ('ward', 'temperature', 'humidity', 'noise_level', 'air_quality', 'timestamp')
    search_fields = ('ward__name',)

admin.site.register(WardReading, WardReadingAdmin)