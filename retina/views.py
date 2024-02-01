from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
from .models import PatientImage, Annotation, PatientInfo, Comment
import random
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .resources import AnnotationResource
from django.urls import reverse
from datetime import datetime

#from django.views.generic import ListView, FormView
#from .admin import AnnotationResource

@login_required
def index(request):
    if request.method == "GET":
        return render(request, 'retina/index.html')
    elif request.method == "POST":
        patient = get_object_or_404(PatientInfo, pk=request.POST["patient_id"])
        return redirect('patient', patient_id=patient.pat_id)

@login_required
def patient(request, patient_id):
    image= get_object_or_404(PatientImage, patient_id=patient_id)
    if request.method == "GET":
        disease_type = ["MA", "NVE", "HAM", "HVE"]     

        my_dict = {"MA": [], "NVE": [], "HAM": [], "HVE": []}
        annotations_qs = Annotation.objects.filter(patient_image=image)
        for annotation in annotations_qs:
            if annotation.disease_type in my_dict:
                my_dict[annotation.disease_type].append(annotation.get_coord())

        processed = Annotation.objects.values("patient_image__patient_id__pat_id").distinct().count()
        total = PatientInfo.objects.all().count()
        context = {
            'patient_img': image,
            'annotations': my_dict,
            "comment": Comment.objects.filter(patient_image=image, disease_type="HVE").first(),
            'disease_type': disease_type,
            "processed": processed,
            "total": total,
        }
        return render(request, 'retina/patient.html', context)
    elif request.method == "POST":
        body = json.loads(request.body)
        disease_type = body.get('disease_type')
        annotations = body.get("annotations")
        if disease_type == "HVE":   
            Comment.objects.update_or_create(
                patient_image=image,
                disease_type=disease_type,
                defaults={"comment": body.get("comment")}
            )
        for annotation in annotations:
            Annotation.objects.update_or_create(
                patient_image=image, 
                disease_type=disease_type, 
                x_cord=annotation["x"], 
                y_cord=annotation["y"], 
                defaults={"radius": annotation["radius"]},
            )
        return HttpResponse("Annotation Saved")
    else:
        return HttpResponse("Error", status_code=400)

#to iterate
@login_required
def next_patient(request, patient_id):
    patients = list(PatientInfo.objects.all())
    options = random.sample(patients, 2)
    if options[0].pat_id == patient_id:
        next = options[1].pat_id
    else:
        next = options[0].pat_id
    return redirect('patient', patient_id=next)

@login_required
def export_data_to_excel(request):
    resource = AnnotationResource()
    dataset = resource.export()

    current_time = datetime.now()
    formatted_date = current_time.strftime("%d-%m-%Y") 
    filename = f"Annotated_Data_{formatted_date}.xlsx"

    response = HttpResponse(dataset.xlsx, content_type='tapplication/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] =  f'attachment; filename="{filename}"'
    return response