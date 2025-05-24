from django.urls import path
from . import views
# from .views import ward_readings_partial

urlpatterns = [
    path('', views.index, name='index'),
    path('ward/<int:ward_id>/', views.ward_conditions, name="ward_conditions")
    # path('htmx/ward-readings/', ward_readings_partial, name='ward_readings_partial'),
]