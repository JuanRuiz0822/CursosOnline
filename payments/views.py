from uuid import uuid4
import hmac
import hashlib
import json

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from enrollments.models import Enrollment
from courses.models import Course
from .models import Payment


class CheckoutView(APIView):
    """Inicia un pago para un curso.
    
    POST /api/payments/checkout/
    Body: {course_id, method: 'card'|'nequi'}
    
    Retorna datos para redirigir a Wompi o completar el pago.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        method = request.data.get("method", "card")  # card | nequi

        if not course_id:
            return Response(
                {"detail": "course_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if method not in ['card', 'nequi']:
            return Response(
                {"detail": "method debe ser 'card' o 'nequi'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(pk=course_id, is_active=True)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Curso no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Solo estudiantes (role == 'student') pueden comprar
        role = getattr(user, "role", None)
        if role != "student":
            return Response(
                {"detail": "Solo estudiantes pueden comprar cursos"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Evitar pagos duplicados si ya está inscrito
        if Enrollment.objects.filter(student=user, course=course).exists():
            return Response(
                {"detail": "Ya estás inscrito en este curso"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generar referencia única
        reference = str(uuid4())
        amount = course.price

        # Crear Payment en estado pending
        payment, created = Payment.objects.get_or_create(
            student=user,
            course=course,
            defaults={
                'amount': amount,
                'currency': 'COP',
                'status': 'pending',
                'provider': 'wompi',
                'method': method,
                'reference': reference,
            }
        )

        if not created and payment.status != 'pending':
            return Response(
                {"detail": "Ya existe un pago para este curso"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # En producción, aquí se llamaría a la API de Wompi
        # Para demo, retornamos datos para simular el flujo
        
        # URL de checkout simulada (en producción sería la URL real de Wompi)
        checkout_url = f"http://localhost:8000/?payment_ref={reference}"

        return Response(
            {
                "reference": reference,
                "amount": str(amount),
                "currency": "COP",
                "provider": "wompi",
                "method": method,
                "checkout_url": checkout_url,
                "public_key": settings.WOMPI_PUBLIC_KEY,
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentStatusView(APIView):
    """Consulta el estado de un pago por referencia.
    
    GET /api/payments/status/?reference=<uuid>
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        reference = request.query_params.get('reference')
        
        if not reference:
            return Response(
                {"detail": "reference es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response(
                {"detail": "Pago no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verificar que el usuario sea el propietario del pago
        if payment.student != request.user:
            return Response(
                {"detail": "No autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "reference": payment.reference,
            "status": payment.status,
            "amount": str(payment.amount),
            "currency": payment.currency,
            "method": payment.method,
            "created_at": payment.created_at,
            "updated_at": payment.updated_at,
        })


@method_decorator(csrf_exempt, name="dispatch")
class WebhookView(APIView):
    """Endpoint para recibir notificaciones de la pasarela Wompi.
    
    POST /api/payments/webhook/
    
    Valida la firma HMAC y actualiza el estado del pago.
    Si status=approved, crea la Enrollment automáticamente.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Webhook simulado para demo. En producción:
        1. Validar firma HMAC con WOMPI_PRIVATE_KEY
        2. Procesar notificación de Wompi
        3. Actualizar Payment.status
        4. Crear Enrollment si approved
        """
        
        # Para demo, aceptamos: reference, status, transaction_id
        reference = request.data.get("reference")
        payment_status = request.data.get("status")  # approved | rejected
        transaction_id = request.data.get("transaction_id", "")

        if not all([reference, payment_status]):
            return JsonResponse(
                {"detail": "reference y status son requeridos"},
                status=400
            )

        if payment_status not in ['approved', 'rejected']:
            return JsonResponse(
                {"detail": "status debe ser 'approved' o 'rejected'"},
                status=400
            )

        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return JsonResponse(
                {"detail": "Pago no encontrado"},
                status=404
            )

        # Actualizar estado del pago
        payment.status = payment_status
        if transaction_id:
            payment.transaction_id = transaction_id
        payment.save()

        # Si fue aprobado, crear Enrollment
        if payment_status == 'approved':
            enrollment, created = Enrollment.objects.get_or_create(
                student=payment.student,
                course=payment.course,
                defaults={'status': 'active'}
            )

        return JsonResponse({"detail": "ok", "reference": reference})
