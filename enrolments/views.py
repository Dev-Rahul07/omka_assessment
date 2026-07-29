from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsStudent, IsAdmin, IsInstructor
from .models import Enrolment
from courses.models import Course
from .serializers import EnrolmentSerializer

class EnrolmentListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated()]

    def get(self, request):
        user = request.user
        if user.role == 'admin':
            enrolments = Enrolment.objects.all()
        elif user.role == 'instructor':
            # Only enrolments for courses they instruct
            enrolments = Enrolment.objects.filter(course__instructor=user)
        else:  # student
            enrolments = Enrolment.objects.filter(student=user)
        serializer = EnrolmentSerializer(enrolments, many=True)
        return Response(serializer.data)

    def post(self, request):
        course_id = request.data.get('course')
        if not course_id:
            return Response({'course': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'course': 'Invalid course'}, status=status.HTTP_400_BAD_REQUEST)
        # Check if already enrolled
        if Enrolment.objects.filter(student=request.user, course=course).exists():
            return Response({'detail': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)
        enrolment = Enrolment.objects.create(student=request.user, course=course)
        serializer = EnrolmentSerializer(enrolment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EnrolmentDetailView(APIView):
    def get_permissions(self):
        # For delete, allow if admin or student themselves
        if request.method == "DELETE":
            return [IsAdmin,IsStudent]
        return [IsAuthenticated()]

    def get_object(self, pk, user):
        try:
            return Enrolment.objects.get(pk=pk)
        except Enrolment.DoesNotExist:
            return None

    def delete(self, request, pk):
        enrolment = self.get_object(pk, request.user)
        if not enrolment:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        # Permissions: admin or the student himself
        if self.check_object_permissions(request,enrolment):
            enrolment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)