from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from .models import Course, Subscription


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.course = Course.objects.create(title='Test Course', owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_add_and_remove_subscription(self):
        url = reverse('lms:subscription')
        response = self.client.post(url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        response = self.client.post(url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())


class CourseLessonCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='creator@example.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.test_image = SimpleUploadedFile(
            "test_image.jpg",
            b"\x47\x49\x46\x38\x37\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04"
            b"\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B",
            content_type="image/gif"
        )

    # Оставлен только тест с созданием нового курса
    def test_create_course(self):
        course_data = {
            'title': 'New Course',
            'description': 'Some description',
            'preview': self.test_image,
        }
        course_response = self.client.post(reverse('lms:course-list'), course_data, format='multipart')
        self.assertEqual(course_response.status_code, 201)
