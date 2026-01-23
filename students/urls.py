from django.urls import path
from .views import register_student, registration_success, student_list, download_students_csv

urlpatterns = [
    path("register/", register_student, name="register"),
    path("success/", registration_success, name="success"),
    path("students/", student_list, name="student_list"),
    path("students/download/", download_students_csv, name="download_students"),
]
