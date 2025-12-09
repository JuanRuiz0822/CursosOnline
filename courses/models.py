from django.db import models
from users.models import Instructor

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('guitar', 'Guitarra'),
        ('piano', 'Piano'),
        ('violin', 'Violín'),
        ('drums', 'Batería'),
        ('singing', 'Canto'),
        ('music_theory', 'Teoría Musical'),
    ]
    
    TYPE_CHOICES = [
        ('online', 'En Línea'),
        ('presencial', 'Presencial'),
        ('hibrido', 'Híbrido'),
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    course_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField(default=0)
    
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    duration_weeks = models.IntegerField()
    total_lessons = models.IntegerField()
    
    schedule = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    rating = models.FloatField(default=5.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()
    duration_minutes = models.IntegerField()
    video_url = models.URLField(blank=True)
    materials = models.FileField(upload_to='materials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - Lección {self.order}"
