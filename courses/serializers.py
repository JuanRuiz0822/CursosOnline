from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'order', 'duration_minutes', 'video_url']

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    instructor_name = serializers.SerializerMethodField()
    instructor_id = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor_name', 'instructor_id', 'category', 
            'course_type', 'level', 'price', 'discount_percentage', 
            'duration_weeks', 'total_lessons', 'rating', 'schedule', 'lessons', 'thumbnail_url'
        ]
    
    def get_instructor_name(self, obj):
        return obj.instructor.user.get_full_name() or obj.instructor.user.username

    def get_instructor_id(self, obj):
        return obj.instructor.id

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            url = obj.thumbnail.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None
