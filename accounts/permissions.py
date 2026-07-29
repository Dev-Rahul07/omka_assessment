from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    role = None
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == self.role)

class IsAdmin(RolePermission):
    role = 'admin'

class IsStudent(RolePermission):
    role = 'student'

class IsInstructor(RolePermission):
    role = 'instructor'

class IsInstructorOfCourse(IsInstructor):
    """Allows access only if the user is the instructor of the course."""
    def has_object_permission(self, request, view, obj):
        course = getattr(obj, 'course', obj)
        return getattr(course, 'instructor', None) == request.user

class IsEnrolledInCourse(IsStudent):
    """Allows access if the student is enrolled in the course."""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'course'):
            course = obj.course
        elif hasattr(obj, 'module'):
            course = obj.module.course
        else:
            return False
        return course.enrolments.filter(student=request.user).exists()
