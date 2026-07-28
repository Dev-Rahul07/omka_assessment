from rest_framework import serializers
from .models import Enrolment

class EnrolmentSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Enrolment
        fields = ['id', 'student', 'course', 'course_title', 'enrolled_at']
        