from django.shortcuts import get_object_or_404, render
from live_data.models import WardReading, Ward,Bed, Patient
from django.http import HttpResponse

# Create your views here.
def index(request):
    # Get the latest WardReading for each ward
    wards = Ward.objects.all()
    beds = Bed.objects.all()
    patients = Patient.objects.all()
    no_of_wards = 0
    no_of_beds=0
    no_of_patients =0
    for ward in wards:
        no_of_wards+=1
    
    for bed in beds:
        no_of_beds+=1
    for patient in patients:
        no_of_patients+=1
    latest_readings = (
        WardReading.objects.order_by('ward', '-timestamp')
        .distinct('ward')
    )
    patients_with_microcontroller=0
    for patient in patients:
        if patient.microcontroller:
            patients_with_microcontroller+=1
            print(patient.microcontroller)


    context = {
        "no_of_wards" : no_of_wards,
        'latest_readings': latest_readings,
        'no_of_beds': no_of_beds,
        'no_of_patients': no_of_patients,
        'monitored_patients': patients_with_microcontroller
    }
    return render(request, 'index.html', context)

# def ward_readings_partial(request):
#     latest_readings = (
#         WardReading.objects.order_by('ward', '-timestamp').distinct('ward')
#     )
#     return render(request, 'partials/ward_readings_partial.html', {'latest_readings': latest_readings})


def ward_conditions(request, ward_id):
    ward = get_object_or_404(Ward, id=ward_id)
    context = {
        "ward": ward
    }

    return render(request, 'ward.html', context)