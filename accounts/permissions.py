from rest_framework.permissions import BasePermission, SAFE_METHODS

# isAdmin Permission
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'



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
        return course.instructor == request.user
