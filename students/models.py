from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    class_name = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        managed = False   # 👈 VERY IMPORTANT
        db_table = 'students_student'
