from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'course_type', 'level', 'instructor', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'rating']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        user = self.request.user
        instructor = getattr(user, 'instructor', None)
        if not instructor:
            # Si no es instructor, denegar creación
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Solo instructores pueden crear cursos')
        serializer.save(instructor=instructor)
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = self.get_object()
        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
