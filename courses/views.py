from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsInstructor, IsInstructorOfCourse
from courses.models import Course, Module
from courses.serializers import CourseSerializer, ModuleSerializer


class CourseListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsInstructor()]
        return [IsAuthenticated()]  # anyone can list

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CourseDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsInstructorOfCourse()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, course)  
        serializer = CourseSerializer(course, data=request.data, partial=True) if request.method == 'PATCH' else CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, course)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ModuleListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsInstructor()]
        return [IsAuthenticated()]  

    def get(self, request):
        course_id = request.query_params.get('course')
        if course_id:
            modules = Module.objects.filter(course_id=course_id)
        else:
            modules = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            course_id = request.data.get('course')
            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                return Response({'course': 'Invalid course id'}, status=status.HTTP_400_BAD_REQUEST)
            # Check instructor owns the course
            if course.instructor != request.user:
                return Response({'detail': 'You do not own this course'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModuleDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsInstructorOfCourse()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Module.objects.get(pk=pk)
        except Module.DoesNotExist:
            return None

    def get(self, request, pk):
        module = self.get_object(pk)
        if not module:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModuleSerializer(module)
        return Response(serializer.data)

    def put(self, request, pk):
        module = self.get_object(pk)
        if not module:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, module)  # instructor check
        serializer = ModuleSerializer(module, data=request.data, partial=True) if request.method == 'PATCH' else ModuleSerializer(module, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        module = self.get_object(pk)
        if not module:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, module)
        if module.submissions.count()>0:
            return Response("you cant delete this module..",status=status.HTTP_400_BAD_REQUEST)
        module.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)