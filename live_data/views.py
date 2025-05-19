from django.shortcuts import render
from live_data.models import WardReading

# Create your views here.
def index(request):
    # Get the latest WardReading for each ward
    latest_readings = (
        WardReading.objects.order_by('ward', '-timestamp')
        .distinct('ward')
    )
    return render(request, 'index.html', {'latest_readings': latest_readings})

