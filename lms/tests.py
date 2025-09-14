from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
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
