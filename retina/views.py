import io
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
import pandas as pd

#from django.views.generic import ListView, FormView
#from .admin import AnnotationResource

@login_required
def index(request):
    return redirect("nextpat")

@login_required
def patient(request, patient_id):
    image= get_object_or_404(PatientImage, patient_id=patient_id)
    if image.patient_id.processed:
        return redirect("nextpat")

    processed = PatientInfo.objects.filter(processed=True).count()
    total = PatientInfo.objects.all().count()

    if processed == total:
        return render(request, 'retina/finished.html')

    if request.method == "GET":
        disease_type = ["MA", "NVE", "HAM", "HVE"]     

        my_dict = {"MA": [], "NVE": [], "HAM": [], "HVE": []}
        annotations_qs = Annotation.objects.filter(patient_image=image)
        for annotation in annotations_qs:
            if annotation.disease_type in my_dict:
                my_dict[annotation.disease_type].append(annotation.get_coord())

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
            image.patient_id.processed = True
            image.patient_id.save()
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
def next_patient(request):
    patients = PatientInfo.objects.filter(processed=False)
    if patients.count() == 0:
        return render(request, 'retina/finished.html')
    next = random.choice(list(patients))
    return redirect('patient', patient_id=next.pat_id)

# @login_required
# def export_data_to_excel(request):
#     resource = AnnotationResource()
#     dataset = resource.export()

#     current_time = datetime.now()
#     formatted_date = current_time.strftime("%d-%m-%Y") 
#     filename = f"Annotated_Data_{formatted_date}.xlsx"

#     response = HttpResponse(dataset.xlsx, content_type='tapplication/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] =  f'attachment; filename="{filename}"'
#     return response


@login_required
def export_data_to_excel(request):
    annotations = Annotation.objects.all()
    comments = Comment.objects.all()

    data_comments = {
        "patient_id": [],
        "disease_type": [],
        "comment": [],
    }
    data_ann = {
        "patient_id": [],
        "disease_type": [],
        "x_cord": [],
        "y_cord": [],
        "radius": [],
    }
    for annotation in annotations:
        data_ann["patient_id"].append(annotation.patient_image.patient_id.pat_id)
        data_ann["disease_type"].append(annotation.disease_type)
        data_ann["x_cord"].append(annotation.x_cord)
        data_ann["y_cord"].append(annotation.y_cord)
        data_ann["radius"].append(annotation.radius)

    for comment in comments:
        data_comments["patient_id"].append(comment.patient_image.patient_id.pat_id)
        data_comments["disease_type"].append(comment.disease_type)
        data_comments["comment"].append(comment.comment)

    df_ann = pd.DataFrame(data_ann)
    df_comments = pd.DataFrame(data_comments)

    df = pd.merge(df_ann, df_comments, on=["patient_id", "disease_type"], how="left")

    current_time = datetime.now()
    formatted_date = current_time.strftime("%d-%m-%Y") 
    filename = f"Annotated_Data_{formatted_date}.xlsx"

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    xlsx_data = output.getvalue()
    response = HttpResponse(xlsx_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response