from rest_framework.permissions import BasePermission, SAFE_METHODS

# isAdmin Permission
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'instructor'

class IsAdminOrStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'student']


class IsInstructorOfCourse(BasePermission):
    """
    Allows access only if the user is the instructor of the course.
    Expects view to have a method get_course() or a course_id in kwargs.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != 'instructor':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'instructor'):
            return obj.instructor == request.user
        elif hasattr(obj, 'course'):
            return obj.course.instructor == request.user
        return False




class IsEnrolledInCourse(BasePermission):
    """
    Allows access if the student is enrolled in the course.
    """
    def has_permission(self, request, view):
        # We'll check object permission for detail views
        return request.user.is_authenticated and request.user.role == 'student'

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'course'):
            course = obj.course
        elif hasattr(obj, 'module'):
            course = obj.module.course
        else:
            return False
        return course.enrolments.filter(student=request.user).exists()
