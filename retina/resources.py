# retina/resources.py
from import_export import resources
from .models import Annotation  # Replace YourModel with your actual model name

class AnnotationResource(resources.ModelResource):
    class Meta:
        model = Annotation
