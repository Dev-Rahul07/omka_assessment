from rest_framework import serializers
from .models import Course, Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            "id",
            "course",
            "title",
            "description",
            "order",
            "created_at",
            "updated_at",
        ]

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.ReadOnlyField(source='instructor.username')
    modules = ModuleSerializer(many=True, read_only=True) #nested serializer    

    class Meta:
        model = Course
        fields = ["id", "title", "description", "instructor", "modules", "created_at", "updated_at"]