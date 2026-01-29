from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
import csv

from .models import Student
from .utils import encrypt_value, decrypt_value


# REGISTER 
@csrf_exempt
def register_student(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Only POST method allowed"
        }, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    name = data.get("name")
    email =data.get("email")
    mobile = data.get("mobile")
    class_name = data.get("class_name")

    if not all([name, email, mobile, class_name]):
        return JsonResponse({
            "error": "All fields are required"
        }, status=400)

    student = Student.objects.create(
        name=name,
        email=encrypt_value(email),
        mobile=encrypt_value(mobile),
        class_name=class_name,
    )

    return JsonResponse({
        "status": "success",
        "student_id": student.id,
        "message": "Student registered successfully"
    }, status=201)


# SUCCESS
def registration_success(request):
    student_id = request.GET.get("id")

    return JsonResponse({
        "status": "success",
        "student_id": student_id
    })



# STUDENT LIST 
def student_list(request):
    students = Student.objects.all()
    data = []

    for student in students:
        try:
            email = decrypt_value(student.email)
            mobile = decrypt_value(student.mobile)
        except Exception:
            # Handles InvalidToken safely
            email = "Decryption failed (invalid key)"
            mobile = "Decryption failed (invalid key)"

        data.append({
            "id": student.id,
            "name": student.name,
            "class": student.class_name,
            "email": email,
            "mobile": mobile,
        })

    return JsonResponse({"students": data})




# CSV DOWNLOAD 
def download_students_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Name", "Class"])

    for student in Student.objects.all():
        writer.writerow([student.id, student.name, student.class_name])

    return response
