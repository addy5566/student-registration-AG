from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
import csv

from .models import Student
from .utils import encrypt_value, decrypt_value


# REGISTER 
def register_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        class_name = request.POST.get("class_name")

        if not all([name, email, mobile, class_name]):
            return render(request, "students/register.html", {
                "error": "All fields are required"
            })

        student = Student.objects.create(
            name=name,
            email=encrypt_value(email),
            mobile=encrypt_value(mobile),
            class_name=class_name,
        )

        try:
            decrypted_email = decrypt_value(student.email)
            send_mail(
                subject="Registration Successful",
                message=f"Hello {name}, your registration ID is {student.id}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[decrypted_email],
                fail_silently=True,  # ✅ IMPORTANT
            )
        except Exception:
            pass

        return redirect("success")

    return render(request, "students/register.html")


# SUCCESS
def registration_success(request):
    student_id = request.GET.get("id")
    return render(request, "students/success.html", {
        "student_id": student_id
    })


# STUDENT LIST 
def student_list(request):
    query = request.GET.get("q")
    class_filter = request.GET.get("class_name")  # ✅ FIXED

    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    if class_filter:
        students = students.filter(class_name=class_filter)

    for student in students:
        try:
            student.email = decrypt_value(student.email)
            student.mobile = decrypt_value(student.mobile)
        except Exception:
            student.email = "Error"
            student.mobile = "Error"

    return render(request, "students/list.html", {
        "students": students
    })


# CSV DOWNLOAD 
def download_students_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Name", "Class"])

    for student in Student.objects.all():
        writer.writerow([student.id, student.name, student.class_name])

    return response
