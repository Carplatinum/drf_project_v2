from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url']

    def validate(self, data):
        validator = VideoUrlValidator(fields=['video_url'])
        validator(data)
        return data


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'preview', 'description',
            'lessons_count', 'lessons', 'is_subscribed'
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
