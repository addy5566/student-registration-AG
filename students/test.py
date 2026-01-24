from django.test import TestCase, Client
from django.urls import reverse
from .models import Student
from .utils import decrypt_value

class StudentFlowTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_complete_student_registration_flow(self):
        """
        This test checks the complete flow:
        1. Register a student
        2. Verify data is saved
        3. Verify encrypted fields can be decrypted
        """

        response = self.client.post(reverse("register"), {
            "name": "Test Student",
            "email": "test@student.com",
            "mobile": "9999999999",
            "class_name": "BCA"
        })

        # Check redirect after successful registration
        self.assertEqual(response.status_code, 302)

        # Check student saved in database
        student = Student.objects.get(name="Test Student")

        self.assertEqual(decrypt_value(student.email), "test@student.com")
        self.assertEqual(decrypt_value(student.mobile), "9999999999")
        self.assertEqual(student.class_name, "BCA")
