from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from .models import CustomUser, Instructor


def user_payload(user: CustomUser):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data or {}
        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        role = (data.get("role") or "student").strip()

        if not username or not password:
            return Response({"detail": "username y password son requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username=username).exists():
            return Response({"detail": "username ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        if email and CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "email ya está en uso"}, status=status.HTTP_400_BAD_REQUEST)
        if role not in ("student", "instructor"):
            role = "student"

        try:
            validate_password(password)
        except DjangoValidationError as e:
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            username=username, email=email, password=password, role=role
        )
        # Crear Instructor si aplica
        if role == "instructor":
            Instructor.objects.create(user=user, specialization="", experience_years=0)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": user_payload(user)}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        if not username or not password:
            return Response({"detail": "username y password son requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": user_payload(user)})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Invalida el token actual
        Token.objects.filter(user=request.user).delete()
        # Crear uno nuevo opcionalmente
        token = Token.objects.create(user=request.user)
        return Response({"detail": "Sesión cerrada", "new_token": token.key})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"user": user_payload(request.user)})
