from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('refunded', 'Reembolsado'),
    ]
    
    PROVIDER_CHOICES = [
        ('wompi', 'Wompi'),
        ('stripe', 'Stripe'),
    ]
    
    METHOD_CHOICES = [
        ('card', 'Tarjeta Crédito/Débito'),
        ('nequi', 'Nequi'),
    ]
    
    # Relaciones
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    
    # Datos del pago
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='COP')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Proveedor y método
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='wompi')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='card')
    
    # Referencias
    reference = models.CharField(max_length=255, unique=True, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'course']  # Un pago por estudiante/curso
    
    def __str__(self):
        return f"Pago {self.id} - {self.student.username} - {self.course.title} ({self.status})"
