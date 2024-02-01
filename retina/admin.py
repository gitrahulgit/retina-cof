from django.contrib import admin
from .models import PatientInfo, PatientImage, Annotation, Comment
from import_export import resources


# Register your models here.

admin.site.register(PatientInfo)
admin.site.register(PatientImage)
admin.site.register(Annotation)
admin.site.register(Comment)

# class AnnotationResource(resources.ModelResource):
#     class Meta:
#         model = Annotation
#         fields = ('patient_image', 'disease_type', 'x_cord', 'y_cord', 'radius')
#         export_order = ('patient_image', 'disease_type', 'x_cord', 'y_cord', 'radius')