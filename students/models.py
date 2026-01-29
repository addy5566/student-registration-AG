from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.TextField()          
    mobile = models.TextField()         
    mobile_hash = models.CharField(max_length=64, unique=True)
    class_name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "students_student"
        

