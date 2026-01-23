from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Student
from .utils import encrypt_value, decrypt_value

# code for register

def register_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        class_name = request.POST.get("class")

    student = Student.objects.create(
        name=name,
        email=encrypt_value(email),
        mobile=encrypt_value(mobile),
        class_name=class_name
        )

        decrypted_email = decrypt_value(student.email)

        send_mail(
            subject="Registration Successful",
            message=f"Hello {name}, your registration ID is {student.id}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[decrypted_email],
            fail_silently=False,
        )

        return redirect(f"/success/?id={student.id}")

    return render(request, "students/register.html")



    # this code is for success of registration
def registration_success(request):
    student_id = request.GET.get("id")
    return render(request, "students/success.html", {
        "student_id": student_id
    })




# this code is for showing list of all students

from django.db.models import Q
from django.shortcuts import render
from .models import Student
from .utils import decrypt_value


def student_list(request):
    query = request.GET.get('q')
    class_filter = request.GET.get('class')

    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    if class_filter:
        students = students.filter(class_name=class_filter)

    # 🔐 SAFE DECRYPTION (CRITICAL FIX)
    for s in students:
        try:
            s.email = decrypt_value(s.email)
            s.mobile = decrypt_value(s.mobile)
        except Exception:
            s.email = "Decryption Error"
            s.mobile = "Decryption Error"

    return render(request, "students/list.html", {
        "students": students
    })


    # This code is for download csv file

def download_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Class'])

    for student in Student.objects.all():
        writer.writerow([student.id, student.name, student.class_name])

    return response



