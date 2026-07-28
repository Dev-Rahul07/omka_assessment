from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    module_title = serializers.ReadOnlyField(source='module.title')

    class Meta:
        model = Submission
        fields = ['id', 'student', 'module', 'module_title', 'content', 'submitted_at', 'updated_at']