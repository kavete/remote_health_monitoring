from django.urls import path
from . import views
# from .views import ward_readings_partial

urlpatterns = [
    path('', views.index, name='index'),
    path('ward/<int:ward_id>/', views.ward_conditions, name="ward_conditions"),
    path("accounts/login/", views.login_view, name="login_url"),
    # path('htmx/ward-readings/stream', views.ward_readings_stream, name='ward_readings_stream'),
    # path('htmx/ward-readings/', ward_readings_partial, name='ward_readings_partial'),
]