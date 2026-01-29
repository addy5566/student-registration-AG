from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import csv

from .models import Student
from .utils import encrypt_value, decrypt_value, hash_value
from .email_service import send_registration_email


# =========================
# REGISTER STUDENT (API)
# =========================
@csrf_exempt
def register_student(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )

    # Parse JSON safely
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    name = data.get("name")
    email = data.get("email")
    mobile = data.get("mobile")
    class_name = data.get("class_name")

    if not all([name, email, mobile, class_name]):
        return JsonResponse(
            {"error": "All fields are required"},
            status=400
        )

    # ✅ HASH for uniqueness
    mobile_hash = hash_value(mobile)

    # ✅ UNIQUE CHECK
    if Student.objects.filter(mobile_hash=mobile_hash).exists():
        return JsonResponse(
            {"error": "Mobile number already registered"},
            status=409
        )

    # ✅ SAVE STUDENT
    student = Student.objects.create(
        name=name,
        email=encrypt_value(email),
        mobile=encrypt_value(mobile),
        mobile_hash=mobile_hash,
        class_name=class_name,
    )

    # ✅ SEND EMAIL (SMTP / external service)
    send_registration_email(
        to_email=email,
        student_id=student.id,
        name=name
    )

    return JsonResponse(
        {
            "status": "success",
            "student_id": student.id,
            "message": "Student registered successfully"
        },
        status=201
    )


# =========================
# REGISTRATION SUCCESS API
# =========================
def registration_success(request):
    student_id = request.GET.get("id")

    return JsonResponse(
        {
            "status": "success",
            "student_id": student_id
        }
    )


# =========================
# STUDENT LIST API
# =========================
def student_list(request):
    students = Student.objects.all()
    data = []

    for student in students:
        try:
            email = decrypt_value(student.email)
            mobile = decrypt_value(student.mobile)
        except Exception:
            email = "Decryption failed"
            mobile = "Decryption failed"

        data.append({
            "id": student.id,
            "name": student.name,
            "class": student.class_name,
            "email": email,
            "mobile": mobile,
        })

    return JsonResponse({"students": data})


# =========================
# CSV DOWNLOAD
# =========================
def download_students_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Name", "Class"])

    for student in Student.objects.all():
        writer.writerow([
            student.id,
            student.name,
            student.class_name
        ])

    return response
