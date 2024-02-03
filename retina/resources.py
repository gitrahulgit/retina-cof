# retina/resources.py
from import_export import resources, fields, widgets
from .models import Annotation, PatientImage, Comment

class AnnotationResource(resources.ModelResource):

    patient_image = fields.Field(column_name='patient_image', attribute='patient_image', widget=widgets.ForeignKeyWidget(PatientImage, 'patient_id'))
    comment = fields.Field(column_name='comment', attribute='comment', widget=widgets.ForeignKeyWidget(Comment, 'patient_image__patient_id'))
    # get comment for unique patient_image and disease_type
    
    class Meta:
        model = Annotation
        fields = ('patient_image', 'disease_type', 'x_cord', 'y_cord', 'radius', 'comment')
        export_order = ('patient_image', 'disease_type', 'x_cord', 'y_cord', 'radius', 'comment')

    def dehydrate_comment(self, annotation):
        related_comment = Comment.objects.filter(patient_image=annotation.patient_image)
        if related_comment.exists():
            return related_comment.first().comment