from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsStudent, IsInstructor, IsAdmin
from .models import Submission
from courses.models import Module
from .serializers import SubmissionSerializer

class SubmissionListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated()]

    def get(self, request):
        user = request.user
        if user.role == 'admin':
            submissions = Submission.objects.all()
        elif user.role == 'instructor':
            # Submissions for modules of courses they instruct
            submissions = Submission.objects.filter(module__course__instructor=user)
        else:  # student
            submissions = Submission.objects.filter(student=user)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        module_id = request.data.get('module')
        if not module_id:
            return Response({'module': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            module = Module.objects.get(pk=module_id)
        except Module.DoesNotExist:
            return Response({'module': 'Invalid module'}, status=status.HTTP_400_BAD_REQUEST)
        # Check student is enrolled in the course
        if not module.course.enrolments.filter(student=request.user).exists():
            return Response({'detail': 'You are not enrolled in this course'}, status=status.HTTP_403_FORBIDDEN)
        
        if Submission.objects.filter(student=request.user, module=module).exists():
            return Response({'detail': 'You already have a submission for this module. Use PUT to update.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user, module=module)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmissionDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Submission.objects.get(pk=pk)
        except Submission.DoesNotExist:
            return None

    def get(self, request, pk):
        submission = self.get_object(pk)
        if not submission:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        if user.role == 'admin':
            pass
        elif user.role == 'instructor' and submission.module.course.instructor == user:
            pass
        elif user.role == 'student' and submission.student == user:
            pass
        else:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data)

    def put(self, request, pk):
        submission = self.get_object(pk)
        if not submission:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        # Only the student who owns it can update
        if request.user != submission.student:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        serializer = SubmissionSerializer(submission, data=request.data, partial=True) if request.method == 'PATCH' else SubmissionSerializer(submission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        submission = self.get_object(pk)
        if not submission:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        # Allow admin or the student
        self.check_object_permissions(request, submission)
        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)