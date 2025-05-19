from django.contrib import admin

# Register your models here.
from .models import Ward, Patient, Bed, Microcontroller, WardReading, PatientVitalReading

class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location')
    search_fields = ('name', 'description') 

admin.site.register(Ward, WardAdmin)

class BedAdmin(admin.ModelAdmin):
    list_display = ('ward', "bed_number")

admin.site.register(Bed, BedAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward', 'bed', 'age', 'weight', 'height', 'microcontroller_display')
    search_fields = ('name', 'ward__name')
    list_filter = ('ward', 'age')

    def microcontroller_display(self, obj):
        mc = obj.microcontroller
        return mc.identifier if mc else None
    microcontroller_display.short_description = 'Microcontroller'

admin.site.register(Patient, PatientAdmin)

class PatientVitalReadingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'body_temperature', 'heartrate', 'timestamp')
    search_fields = ('patient',)

admin.site.register(PatientVitalReading, PatientVitalReadingAdmin)

class MicrocontrollerAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'bed', 'installed_on')
    search_fields = ('name', 'identifier',)
    

admin.site.register(Microcontroller,MicrocontrollerAdmin)

class WardReadingAdmin(admin.ModelAdmin):
    list_display = ('ward', 'temperature', 'humidity', 'timestamp')
    search_fields = ('ward__name',)

admin.site.register(WardReading, WardReadingAdmin)