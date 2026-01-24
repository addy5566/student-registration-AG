from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect("register")  # redirect by name (IMPORTANT)

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("students.urls")),
]
