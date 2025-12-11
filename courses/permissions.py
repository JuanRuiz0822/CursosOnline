from rest_framework import permissions


class IsInstructorOwnerOrReadOnly(permissions.BasePermission):
    """Permite solo al instructor dueño editar el curso; lectura abierta."""

    def has_object_permission(self, request, view, obj):
        # Lecturas siempre permitidas
        if request.method in permissions.SAFE_METHODS:
            return True

        # Debe estar autenticado
        user = request.user
        if not user or not user.is_authenticated:
            return False

        instructor = getattr(user, "instructor", None)
        return instructor is not None and obj.instructor_id == instructor.id
