from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import export_data_to_excel
#app_name = "retina"

urlpatterns = [
    path("", views.index, name="index"),
    path("patient/<str:patient_id>", views.patient, name="patient"),
    path("next/<str:patient_id>", views.next_patient, name="nextpat"),
    path("export/",export_data_to_excel, name="export_data_to_excel"),
    ]
