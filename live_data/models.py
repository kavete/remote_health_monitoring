from django.db import models


class Ward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Bed(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="beds")
    bed_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ward", "bed_number"], name="unique_bed_per_ward")
        ]

    def __str__(self):
        return f"{self.bed_number} in {self.ward}"

class Microcontroller(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True)
    bed = models.OneToOneField(Bed, on_delete=models.CASCADE, related_name="microcontroller")
    installed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} at {self.bed.ward.name} {self.bed.bed_number}"
    

class Patient(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='patients')
    bed = models.OneToOneField(Bed, on_delete=models.CASCADE, related_name="patient")
    age = models.IntegerField()
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)


    @property
    def microcontroller(self):
        """Returns the microcontroller assigned to the patient's bed, if any."""
        return getattr(self.bed, 'microcontroller', None)
    
    def __str__(self):
        return f"{self.name} Bed: {self.bed.bed_number}"
    

class WardReading(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='ward_conditions')
    microcontroller = models.ForeignKey(Microcontroller, on_delete=models.CASCADE, related_name="ward_readings")
    temperature = models.FloatField()
    humidity = models.FloatField()
    # noise_level = models.FloatField()
    # air_quality = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WardReading {self.ward.name} at {self.timestamp}"
    
class PatientVitalReading(models.Model):
    # microcontroller = models.ForeignKey(Microcontroller, on_delete=models.CASCADE, related_name='vital_readings')
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="patient_vital_reading")
    timestamp = models.DateTimeField(auto_now_add=True)
    oxygen_saturation = models.FloatField()
    body_temperature = models.FloatField()
    heartrate = models.IntegerField()

    def __str__(self):
        return f"Vitals from {self.microcontroller} at {self.timestamp}"
