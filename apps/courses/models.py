from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    par = models.IntegerField()

    # Additional fields for the Course model
    # description = models.TextField()  # Detailed description of the golf course
    # image = models.ImageField(upload_to='course_images/')  # Image representing the golf course
    # rating = models.FloatField()  # Rating or popularity of the golf course
    # length = models.IntegerField()  # Length of the golf course
    # architect = models.CharField(max_length=100)  # Name of the golf course architect/designer
    # established_date = models.DateField()  # Date when the golf course was established
    # website = models.URLField()  # Website URL of the golf course
    # phone_number = models.CharField(max_length=20)  # Contact phone number for the golf course
    # is_public = models.BooleanField(default=True)  # Indicates if the golf course information is publicly accessible

    def __str__(self):
        return self.name

