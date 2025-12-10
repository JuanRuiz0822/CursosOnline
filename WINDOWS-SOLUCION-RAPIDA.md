# 🚀 SOLUCIÓN INMEDIATA PARA TU CASO (Windows)

## 📍 TU SITUACIÓN ACTUAL

```
Sistema: Windows
Ruta: C:\Users\SENA\Desktop\musicschool
Shell: Git Bash o PowerShell (INCORRECTO)
Error: venv/bin/activate no encontrado (ESPERADO en Windows)
```

---

## ✅ SOLUCIÓN EN 5 MINUTOS

### PASO 1: Cierra todo

- Cierra Git Bash / PowerShell
- Presiona `Windows + R`
- Escribe: `cmd`
- Presiona `Enter`

### PASO 2: Navega al proyecto

```batch
cd C:\Users\SENA\Desktop\musicschool
```

Verifica:
```batch
dir
```

Debes ver carpetas como: `courses`, `payments`, `musicschool`, etc.

### PASO 3: Elimina carpeta venv anterior (corrupta)

```batch
rmdir /s venv
```

Presiona `Y` y `Enter`

### PASO 4: Crea novo virtualenv (CORRECTO PARA WINDOWS)

```batch
python -m venv venv
```

**Espera ~30 segundos a que termine**

### PASO 5: Activa (CORRECTO PARA WINDOWS)

```batch
venv\Scripts\activate
```

**IMPORTANTE:** La ruta es `\Scripts\` en Windows, NO `/bin/`

Deberías ver:
```
(venv) C:\Users\SENA\Desktop\musicschool>
```

Si ves `(venv)` al inicio, ✅ **ESTÁ ACTIVADO CORRECTAMENTE**

### PASO 6: Instala dependencias

```batch
pip install requests python-dotenv django djangorestframework
```

### PASO 7: Verificar que todo está bien

```batch
python --version
pip list
```

Debes ver en la lista:
- `requests`
- `python-dotenv`
- `Django`
- `djangorestframework`

---

## 📝 CREAR ARCHIVO .env

### Opción A: Con CMD

```batch
# Crea el archivo con contenido
(
  echo WOMPI_PUBLIC_KEY=pub_test_xxxxx
  echo WOMPI_PRIVATE_KEY=priv_test_xxxxx
  echo WOMPI_ENVIRONMENT=test
  echo FRONTEND_URL=http://localhost:8000
  echo SECRET_KEY=your-secret-key-here
  echo DEBUG=True
  echo DATABASE_URL=sqlite:///db.sqlite3
) > .env
```

### Opción B: Manual

1. Abre Notepad
2. Copia:
```
WOMPI_PUBLIC_KEY=pub_test_xxxxx
WOMPI_PRIVATE_KEY=priv_test_xxxxx
WOMPI_ENVIRONMENT=test
FRONTEND_URL=http://localhost:8000
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```
3. Guardas como: `.env` (en la carpeta del proyecto)

---

## 🗄️ MIGRACIONES

```batch
python manage.py makemigrations
python manage.py migrate
```

---

## 👥 CREAR USUARIOS DE PRUEBA

```batch
python manage.py shell
```

Dentro del shell, copia esto:
```python
from django.contrib.auth import get_user_model
from users.models import Instructor
from courses.models import Course

User = get_user_model()

user_inst = User.objects.create_user('instructor@test.com', 'password123')
instructor = Instructor.objects.create(user=user_inst)

user_stu = User.objects.create_user('student@test.com', 'password123')

course = Course.objects.create(
    title="Guitarra Test",
    description="Test course",
    instructor=instructor,
    category="guitar",
    course_type="online",
    level="beginner",
    price=50000,
    discount_percentage=10,
    duration_weeks=8,
    total_lessons=24,
    schedule="On demand",
    is_active=True
)

print("✓ Done!")
exit()
```

---

## 🚀 EJECUTAR SERVIDOR

```batch
python manage.py runserver
```

Verás:
```
Starting development server at http://127.0.0.1:8000/
```

---

## ✅ AHORA DESCARGA LOS ARCHIVOS TÉCNICOS

Desde la interfaz de chat, descarga:

1. **backend-implementacion.md** - Código Python
2. **plan-tecnico.md** - Arquitectura
3. **guia-rapida.md** - Pasos

---

## 📝 ACTUALIZAR ARCHIVOS DJANGO

### 1. courses/permissions.py (CREAR)

```python
from rest_framework import permissions

class IsInstructorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user.instructor
```

### 2. payments/wompi_client.py (CREAR)

*Copia el código completo de backend-implementacion.md*

### 3. payments/serializers.py (CREAR)

```python
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
```

### 4. payments/urls.py (CREAR)

```python
from django.urls import path
from .views import CheckoutView, WebhookView, PaymentStatusView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('status/<str:reference>/', PaymentStatusView.as_view(), name='status'),
]
```

### 5. settings.py (ACTUALIZAR)

Al final del archivo, agrega:
```python
from dotenv import load_dotenv
load_dotenv()

WOMPI_PUBLIC_KEY = os.getenv('WOMPI_PUBLIC_KEY')
WOMPI_PRIVATE_KEY = os.getenv('WOMPI_PRIVATE_KEY')
WOMPI_ENVIRONMENT = os.getenv('WOMPI_ENVIRONMENT', 'test')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8000')

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://checkout.wompi.co",
]
```

### 6. musicschool/urls.py (ACTUALIZAR)

En `urlpatterns`, agrega:
```python
path('api/payments/', include('payments.urls')),
```

### 7. courses/views.py (ACTUALIZAR)

En `CourseViewSet`, agrega:
```python
from courses.permissions import IsInstructorOwnerOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsInstructorOwnerOrReadOnly
    ]
```

---

## ✨ LISTO

Ahora tienes:
- ✅ Virtualenv activado (Windows correcto)
- ✅ Dependencias instaladas
- ✅ .env creado
- ✅ Archivos básicos creados
- ✅ Migraciones ejecutadas
- ✅ Usuarios de prueba
- ✅ Servidor corriendo

**Solo falta copiar el código Python de backend-implementacion.md a los archivos**

---

## 🎯 SIGUIENTE: OBTENER CREDENCIALES WOMPI

1. Ve a: https://dashboard.wompi.co
2. Sign Up
3. Verifica email
4. Settings → API Keys
5. Copia claves SANDBOX
6. Actualiza .env:
   - WOMPI_PUBLIC_KEY=tu_clave_publica
   - WOMPI_PRIVATE_KEY=tu_clave_privada

---

**¿Dudas? Lee: WINDOWS-GUIA.md** 🚀

