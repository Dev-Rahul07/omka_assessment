from django.db import models
from django.conf import settings
from courses.models import Course

# Enrolment Model
class Enrolment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrolments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') # Basically mean that the student will not able enrol twice for the same course

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"