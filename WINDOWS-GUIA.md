# 🪟 GUÍA PARA WINDOWS - Ejecución Correcta

## ❌ PROBLEMA CON BASH EN WINDOWS

Si estás en Windows y usaste `bash install.sh`, obtendrás errores de rutas como:

```
/c/Users/SENA/Desktop/musicschool/venv/bin/activate: No such file or directory
```

**Esto es porque bash y Windows usan rutas diferentes.**

---

## ✅ SOLUCIÓN 1: USAR CMD (Recomendado)

### Paso 1: Abre CMD (NO PowerShell, NO Git Bash)

```
Windows + R
cmd
Enter
```

### Paso 2: Navega a tu proyecto

```batch
cd C:\Users\SENA\Desktop\musicschool
```

Verifica que estés en la ruta correcta:
```batch
dir
```

Deberías ver archivos como: `manage.py`, `courses/`, `payments/`, etc.

### Paso 3: Crea virtualenv

```batch
python -m venv venv
```

**Espera a que termine (~30 segundos)**

Verifica que se creó:
```batch
dir venv
```

### Paso 4: Activa virtualenv

```batch
venv\Scripts\activate
```

Verás:
```
(venv) C:\Users\SENA\Desktop\musicschool>
```

### Paso 5: Instala dependencias

```batch
pip install requests python-dotenv
```

### Paso 6: Crea archivo .env

```batch
# Si tienes editor de texto, abre:
# C:\Users\SENA\Desktop\musicschool\.env

# Y copia esto:
WOMPI_PUBLIC_KEY=pub_test_xxxxx
WOMPI_PRIVATE_KEY=priv_test_xxxxx
WOMPI_ENVIRONMENT=test
FRONTEND_URL=http://localhost:8000
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Paso 7: Ejecuta migraciones

```batch
python manage.py makemigrations
python manage.py migrate
```

### Paso 8: Crea usuarios de prueba

```batch
python manage.py shell
```

En el shell, copia esto:
```python
from django.contrib.auth import get_user_model
from users.models import Instructor
from courses.models import Course

User = get_user_model()

# Crear instructor
user_inst = User.objects.create_user('instructor@test.com', 'password123')
instructor = Instructor.objects.create(user=user_inst)

# Crear estudiante
user_stu = User.objects.create_user('student@test.com', 'password123')

# Crear curso
course = Course.objects.create(
    title="Guitarra Test",
    description="Aprende guitarra",
    instructor=instructor,
    category="guitar",
    course_type="online",
    level="beginner",
    price=50000,
    discount_percentage=10,
    duration_weeks=8,
    total_lessons=24,
    schedule="Bajo demanda",
    is_active=True
)

print("✓ Usuarios y curso creados")
exit()
```

### Paso 9: Inicia servidor

```batch
python manage.py runserver
```

Verás:
```
Starting development server at http://127.0.0.1:8000/
```

### Paso 10: En otra ventana CMD, dentro del proyecto activado

```batch
cd C:\Users\SENA\Desktop\musicschool
venv\Scripts\activate
```

Luego prueba endpoints:
```batch
# Obtener token del instructor
curl -X POST http://localhost:8000/api-token-auth/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"instructor@test.com\",\"password\":\"password123\"}"
```

---

## ✅ SOLUCIÓN 2: USAR EL SCRIPT WINDOWS .bat

Si prefieres automatización en Windows:

### Paso 1: Descarga el script

```
install-windows.bat
```

### Paso 2: Colócalo en la raíz de tu proyecto

```
C:\Users\SENA\Desktop\musicschool\install-windows.bat
```

### Paso 3: Ejecuta en CMD

```batch
cd C:\Users\SENA\Desktop\musicschool
install-windows.bat
```

**Automáticamente:**
- ✓ Verifica Python
- ✓ Crea virtualenv
- ✓ Instala dependencias
- ✓ Crea .env
- ✓ Crea archivos Python base

---

## 🎯 RESUMEN PARA WINDOWS

### Comando 1: Crear virtualenv
```batch
python -m venv venv
```

### Comando 2: Activar virtualenv
```batch
venv\Scripts\activate
```

### Comando 3: Instalar dependencias
```batch
pip install requests python-dotenv django djangorestframework
```

### Comando 4: Crear .env
```batch
# Abre archivo .env con Notepad y copia las variables
```

### Comando 5: Migraciones
```batch
python manage.py makemigrations
python manage.py migrate
```

### Comando 6: Crear usuarios
```batch
python manage.py shell
# Copia el código de creación de usuarios
```

### Comando 7: Ejecutar servidor
```batch
python manage.py runserver
```

---

## 📝 ESTRUCTURA CORRECTA PARA WINDOWS

```
C:\Users\SENA\Desktop\musicschool\
├── venv\                          ← Virtualenv (Windows)
│   └── Scripts\                   ← Scripts Windows (NO bin/)
│       ├── activate.bat           ← Activador Windows
│       ├── python.exe
│       └── pip.exe
├── courses\
│   ├── permissions.py            ← CREAR
│   └── ...
├── payments\
│   ├── wompi_client.py           ← CREAR
│   ├── serializers.py            ← CREAR
│   ├── urls.py                   ← CREAR
│   └── ...
├── musicschool\
│   ├── settings.py               ← MODIFICAR
│   ├── urls.py                   ← MODIFICAR
│   └── ...
├── .env                          ← CREAR
├── manage.py
└── db.sqlite3
```

---

## ✨ DIFERENCIAS WINDOWS vs LINUX/MAC

| Aspecto | Linux/Mac | Windows |
|---------|-----------|---------|
| **Virtualenv path** | `venv/bin/activate` | `venv\Scripts\activate.bat` |
| **Activar** | `source venv/bin/activate` | `venv\Scripts\activate.bat` |
| **Separador ruta** | `/` | `\` |
| **Comando shell** | `bash script.sh` | `script.bat` o CMD |
| **Curl sintaxis** | `curl ... -d '{...}'` | `curl ... -d "{...}"` o PowerShell |

---

## 🐛 SOLUCIONAR ERRORES COMUNES EN WINDOWS

### Error: "Python no reconocido"

**Solución:**
1. Ve a: https://www.python.org/downloads/
2. Descarga Python 3.9+
3. **Marca:** "Add Python to PATH"
4. Instala
5. Reinicia CMD
6. Verifica: `python --version`

### Error: "No such file or directory"

**Solución:**
- No uses `bash`, usa `CMD.exe`
- Usa barras invertidas: `venv\Scripts\activate`
- No uses `/c/Users/`, usa `C:\Users\`

### Error: "venv: command not found"

**Solución:**
```batch
# Windows usa:
python -m venv venv

# NO:
python3 -m venv venv
```

### Error: "Permission denied"

**Solución:**
```batch
# Ejecuta CMD como administrador
# Botón derecho en CMD → Ejecutar como administrador
```

### Error: "Port 8000 already in use"

**Solución:**
```batch
# Usa otro puerto
python manage.py runserver 8001
```

---

## 📚 ARCHIVOS DESCARGABLES AJUSTADOS PARA WINDOWS

He creado versiones de Windows para estos scripts:

✓ **install-windows.bat** - Instalación automática (descarga arriba)
✓ **run-windows.bat** - Ejecutar servidor

---

## ✅ CHECKLIST PARA WINDOWS

- [ ] Abierto CMD (no PowerShell, no Bash)
- [ ] Navegué a carpeta correcta
- [ ] Ejecuté: `python -m venv venv`
- [ ] Ejecuté: `venv\Scripts\activate`
- [ ] Ejecuté: `pip install requests python-dotenv`
- [ ] Creé archivo .env
- [ ] Ejecuté: `python manage.py makemigrations`
- [ ] Ejecuté: `python manage.py migrate`
- [ ] Ejecuté: `python manage.py shell` y creé usuarios
- [ ] Ejecuté: `python manage.py runserver`
- [ ] Accedí a: http://localhost:8000
- [ ] ✅ Sistema funcionando

---

## 🎯 PRÓXIMOS PASOS EN WINDOWS

1. **Descargar documentación técnica** desde interfaz
2. **Copiar código Python** de `backend-implementacion.md`
3. **Actualizar archivos** Django manualmente
4. **Ejecutar servidor** y probar

---

**¡Ya tienes todo para ejecutar en Windows correctamente! 🚀**

