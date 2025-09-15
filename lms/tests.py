from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from .models import Course, Subscription, Lesson


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

    def test_create_course_and_lesson_with_valid_youtube_url(self):
        course_data = {'title': 'New Course', 'description': 'Some description'}
        course_response = self.client.post(reverse('lms:course-list'), course_data)
        self.assertEqual(course_response.status_code, 201)
        course_id = course_response.data['id']

        lesson_data = {
            'title': 'Lesson 1',
            'description': 'Lesson desc',
            'preview': '',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        lesson_response = self.client.post(reverse('lms:lesson-list'), lesson_data)
        self.assertEqual(lesson_response.status_code, 201)

    def test_create_lesson_invalid_video_url(self):
        lesson_data = {
            'title': 'Invalid URL Lesson',
            'description': 'Testing bad URL',
            'preview': '',
            'video_url': 'https://vimeo.com/123456'
        }
        response = self.client.post(reverse('lms:lesson-list'), lesson_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('В поле', str(response.data))

    def test_update_lesson_video_url(self):
        course = Course.objects.create(title='Temp Course', owner=self.user)
        lesson = Lesson.objects.create(
            title='Initial Lesson',
            description='desc',
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=course,
            preview=''
        )
        update_data = {'video_url': 'https://youtu.be/abc123'}
        response = self.client.patch(reverse('lms:lesson-detail', args=[lesson.id]), update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['video_url'], update_data['video_url'])

    def test_delete_course_and_lesson(self):
        course = Course.objects.create(title='Delete Course', owner=self.user)
        lesson = Lesson.objects.create(
            title='Delete Lesson',
            owner=self.user,
            course=course,
            preview='',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        course_response = self.client.delete(reverse('lms:course-detail', args=[course.id]))
        self.assertIn(course_response.status_code, [204, 200])
        lesson_response = self.client.delete(reverse('lms:lesson-detail', args=[lesson.id]))
        self.assertIn(lesson_response.status_code, [204, 200])
