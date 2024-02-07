# Guía Básica de Django
Para aquellos que están empezando Django desde 0, está guía es para tí

## Primeros pasos
### Instalar Python (Windows)
Instala la última version de python desde su [página oficial](https://www.python.org/downloads/)
al momento de instalar haz click en agregar a path para que puedas ejecutarlo desde la consola.
![Instalación de Python](resources/instalar_python.png)

### Chequear instalación de python
En windows abre el cmd o powershell y coloca

```powershell
py --version
```

![Versión de Python](resources/version_python.png)

### (Opcional) Instalar Visual Studio Code 

[Página Oficial](https://code.visualstudio.com/)

### Crear carpeta del proyecto

Crea la carpeta donde estará tu proyecto Django, luego abre el cmd y ve a la carpeta que creaste
![Cambiar carpeta en CMD](resources/cd_cmd.png)

### Crear entorno virtual

Crea tu entorno virtual colocando el cmd
```powershell
py -m venv venv
```

### Activa el entorno virtual 

Esto es necesario de hacer cada vez que quieras usar el proyecto

> **Tip:** Usa la tecla tab para autocompletar el comando

```powershell
venv\Scripts\activate
```
![Entorno Virtual en CMD](resources/venv_cmd.png)


### Instalar Django

Coloca el comando 
```powershell
py -m pip install Django
```
![Instalar Django](resources/django_cmd.png)


### Crea tu proyecto Django

Con el siguiente comando crearas la estructura minima necesaria para correr Django

```cmd
py -m django startproject mi_proyecto
```

### Corriendo el proyecto

Accede a la carpeta mi_proyecto desde el cmd 
```cmd
cd mi_proyecto
```
Y coloca este comando para ejecutar django:

```cmd
py manage.py runserver
```
![Start Django cmd](resources/django_start_cmd.png)

Ahora puedes acceder a tu aplicación abriendo el enlace http://127.0.0.1:8000/ en tu navegador.


¡Felicidades acabas de crear tu primer proyecto hecho en Django!
![Start Django](resources/django_start.png)

## Creando un inicio de sesión

Al crear django por default usa una base de datos SQLite, y también trae unas tablas por defecto necesarias para el funcionamiento de Django. Una de estas tablas es `User` que la puedes usar para crear usuarios en tu aplicación.

### Correr migraciones

Lo primero que tienes que hacer para que las tablas que necesita Django se creen en la base de datos es correr las migraciones (si no entiendes este concepto más adelante se explicará). El comando es
```cmd
py manage.py migrate
```
![Django Migrate](resources/django_migrate.png)


### Crear nueva app

Actualmente los archivos generados por Django son de configuración general, pero necesitamos crear nuevas apps (o puedes llamarlo módulos). Esto se hace con el comando

```cmd
python manage.py startapp auth
```

Aquí crearemos la app auth (puedes ponerle cualquier nombre). Para hacer lo que tenga que ver con registro/login.

### Crear nuestra primera vista

Para crear nuestro primero Hola Mundo accedemos al archivo auth/views.py  y colocamos este código:
```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hola Mundo")
```
> **Tip:** Recuerda guardar los archivos cada vez que lo edites

Para acceder a la vista que creamos necesitamos crear un archivo llamado `urls.py` dentro de la carpeta `auth`, este archivo debe contener:
```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```
Luego editamos el archivo `mi_proyecto/urls.py` para que nos quede así:
```python
from django.contrib import admin
from django.urls import include, path # Actualizado

urlpatterns = [
    path("", include("auth.urls")), # Actualizado
    path("admin/", admin.site.urls),
]
```

Luego si recargamos la página http://127.0.0.1:8000/  veremos nuestra vista
![Hola Mundo](resources/hola_mundo.png)

### Crear los templates

Para usar archivos html necesitamos crear la carpeta `templates`, por default django busca la carpeta `templates` en cada una de las apps instaladas. Este comportamiento lo cambiaremos para que busque la carpeta templates en el top level de nuestro proyecto (al lado del manage.py). Para esto editamos `mi_proyecto/settings.py` y vamos al apartado donde dice TEMPLATES, y lo editamos para que nos quede así
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"], # Actualizado
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
```
Luego creamos la carpeta templates para que nos quede así

![Templates folder](resources/templates_folder.png)

### Crear la vista login
Volvemos a `auth/views.py` y agregamos una vista para el Login, pero esta vez usando una clase en vez de una función. (Puedes usar cualquiera de los dos según te convenga)
```python
from django.views import View


def index(request):
    return HttpResponse("Hola Mundo")

# --Actualización--
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
```
> **Tip:** En Python se suele usar PascalCase para nombrar clases (Inicial de cada palabra en mayúscula. Ej: LoginView)  y snake_case para nombrar variables y funciones (todas las letras minúsculas, separadas por barra baja `_`. Ej: login_view )

Aquí nuestra vista va a renderizar el archivo `login.html` que debe estar dentro de la carpeta `auth` que a su vez debe estar dentro de la carpeta `templates`. Por lo que procedemos a crear dicha carpeta `auth` y dicho archivo `login.html`. Quedando `templates/auth/login.html`

![Templates folder](resources/templates_login.html.png)

En este archivo `templates/auth/login.html` vamos a crear un formulario sencillo para iniciar sesión
```html
<h1>Inicio de sesión</h1>
<form action="" method="post">
    {% csrf_token %}
    <div>
        <label>
            Usuario
            <input type="text" name="username">
        </label>
    </div>
    <div>
        <label>
            Contraseña
            <input type="password" name="password">
        </label>
    </div>
    <button type="submit">Enviar</button>
</form>
```
> **Nota:** la etiqueta `{% csrf_token %}` tiene que ir obligatoriamente en los formularios con `method="post"`. De lo contrario dará error (Está es una medida de seguridad de Django contra ataques CSRF)

Agregamos nuestra vista a nuestro archivo de rutas `auth/urls.py` (cuando usamos una clase tenemos que añadir el `.as_view()`)

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"), #Actualizado
]
```

Y ahora vamos a ver como quedo nuestro login en http://127.0.0.1:8000/login

![Login](resources/login_page.png)
> **Tip:** Puedes añadir CSS a tu gusto ;)

### Procesar el formulario

Ahora vamos a editar nuestra vista para procesar la información del formulario con el método POST. `auth/views.py`

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout # Actualización
from django.views import View


def index(request):
    return HttpResponse("Hola Mundo")


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
    # --- Actualización ---
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Has iniciado sesión")
        else:
            return HttpResponse("Credenciales inválidas")
```

Aquí al hacer post nuestro formulario creamos la función post de nuestra vista, aquí recuperamos los datos del formulario, luego usaremos la función de Django `authenticate`, que solicita como parámetros la petición del usuario, el nombre de usuario y la contraseña, devolviendo el usuario si existe o Nulo si no existe. Luego chequeamos si el usuario no es nulo entonces procedemos a hacer el login, sino le diremos que tiene algún dato inválido.

Pero.... Un momento, ¿Como creamos el usuario que va a hacer login?

### Crear la vista de Registro

Agregamos la vista de registro a nuestro archivo `auth/views.py`

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User # Actualización

def index(request):
    return HttpResponse("Hola Mundo")


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Has iniciado sesión")
        else:
            return HttpResponse("Credenciales inválidas")


# --- Actualización ---
class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponse("Usuario creado")
```
Aquí usamos el model User (que es el usuario default de Django) con su función create_user para crear un nuevo usuario con los datos recibidos del POST. 

> **Nota:** los parámetros `username` y `password` son obligatorios en la función `create_user`, sin embargo el modelo `User` tiene más campos opcionales que puedes consultar [aquí](https://docs.djangoproject.com/es/5.0/ref/contrib/auth/) 

Aquí creamos un html prácticamente idéntico al de login. Este es `templates/auth/register.html`
```html
<h1>Registro de Usuario</h1>
<form action="" method="post">
    {% csrf_token %}
    <div>
        <label>
            Usuario
            <input type="text" name="username">
        </label>
    </div>
    <div>
        <label>
            Contraseña
            <input type="password" name="password">
        </label>
    </div>
    <button type="submit">Enviar</button>
</form>
<a href="/login">Iniciar sesión</a>
```

No nos olvidemos de agregar la vista que creamos a nuestras rutas `auth/urls.py` 

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"), # Actualización
]

```
Y ya podemos probar nuestra aplicación en http://127.0.0.1:8000/register