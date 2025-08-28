from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_url = models.URLField()

    def __str__(self):
        return f"{self.title} (Course: {self.course.title})"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
