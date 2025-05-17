from django.db import models


class Ward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='patients')
    bed_number = models.CharField(max_length=10)
    age = models.IntegerField()
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} Bed: {self.bed_number}"
    

class Microcontroller(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True)
    patient = models.OneToOneField(Patient,on_delete=models.CASCADE, related_name='microcontroller')
    installed_on = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name


class WardReading(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='ward_conditions')
    temperature = models.FloatField()
    humidity = models.FloatField()
    noise_level = models.FloatField()
    air_quality = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WardReading {self.ward.name} at {self.timestamp}"
    
class PatientVitalReading(models.Model):
    microcontroller = models.ForeignKey(Microcontroller, on_delete=models.CASCADE, related_name='vital_readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    oxygen_saturation = models.FloatField()
    body_temperature = models.FloatField()
    heartrate = models.IntegerField()

    def __str__(self):
        return f"Vitals from {self.microcontroller} at {self.timestamp}"


   
    