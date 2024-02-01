from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PatientInfo(models.Model):
    pat_id = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.pat_id  

class PatientImage(models.Model):
    patient_id = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)
    img_type = models.CharField(max_length=20)
    img_link = models.URLField(max_length=200) 
    
    def __str__(self):
        return f"{self.patient_id} -- {self.img_type}"
    
class Annotation(models.Model):
    patient_image = models.ForeignKey(PatientImage, on_delete=models.CASCADE)
    disease_type= models.CharField(max_length=20)
    x_cord = models.FloatField(max_length=10)
    y_cord = models.FloatField(max_length=10)
    radius = models.FloatField(max_length=10)
    
    def get_coord(self):
        return {"x": self.x_cord, "y": self.y_cord, "radius": self.radius}
    
    def __str__(self):
        return '{}/{}/{}'.format(self.x_cord, self.y_cord, self.radius)
    

class Comment(models.Model):
    patient_image = models.ForeignKey(PatientImage, on_delete=models.CASCADE)
    disease_type = models.CharField(max_length=20)
    comment = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return "{}/{}".format(self.disease_type, self.comment)

    