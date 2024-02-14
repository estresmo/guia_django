# Guía Básica de Django
Para aquellos que están empezando Django desde 0, está guía es para tí

<!-- toc -->

- [Primeros pasos](#primeros-pasos)
  * [Instalar Python (Windows)](#instalar-python-windows)
  * [Chequear instalación de python](#chequear-instalacion-de-python)
  * [(Opcional) Instalar Visual Studio Code](#opcional-instalar-visual-studio-code)
  * [Crear carpeta del proyecto](#crear-carpeta-del-proyecto)
  * [Crear entorno virtual](#crear-entorno-virtual)
  * [Activa el entorno virtual](#activa-el-entorno-virtual)
  * [Instalar Django](#instalar-django)
  * [Crea tu proyecto Django](#crea-tu-proyecto-django)
  * [Corriendo el proyecto](#corriendo-el-proyecto)
- [Creando un inicio de sesión](#creando-un-inicio-de-sesion)
  * [Correr migraciones](#correr-migraciones)
  * [Crear nueva app](#crear-nueva-app)
  * [Crear nuestra primera vista](#crear-nuestra-primera-vista)
  * [Crear los templates](#crear-los-templates)
  * [Crear la vista login](#crear-la-vista-login)
  * [Procesar el formulario](#procesar-el-formulario)
  * [Crear la vista de Registro](#crear-la-vista-de-registro)
  * [Repaso](#repaso)
- [Completando el CRUD](#completando-el-crud)
  * [Creando la vista de Usuarios](#creando-la-vista-de-usuarios)
  * [Zona horaria (opcional)](#zona-horaria-opcional)
  * [Haciendo la vista editar](#haciendo-la-vista-editar)
  * [Eliminar](#eliminar)
  * [Repaso](#repaso-1)
- [Arreglando rutas](#arreglando-rutas)
  * [Añadiendo algo de seguridad](#anadiendo-algo-de-seguridad)

<!-- tocstop -->

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

### Repaso

Hay datos que necesitan ser iguales para que nuestra aplicación Django funcione correctamente, algunos de estos son:

Relación parámetro `name` en los input con el `request.POST`
![SameView1](resources/same_view_1.png)
Relación entre el nombre de las vistas con las rutas
![SameView2](resources/same_view_2.png)
Relación de las variables con los parámetros de una función
![SameView3](resources/same_view_3.png)
Relación de la ruta en python y la del navegador
![SameView4](resources/same_view_4.png)

> **Recomendación:** Puedes practicar cambiando el nombre de las variables/clases/funciones que se relacionan.

## Completando el CRUD
Ya vimos como crear un usuario y hacer un login con el mismo, pero ahora veremos como podemos hacer para ver los usuarios que creamos y pode editarlos

### Creando la vista de Usuarios
Para obtener todos los registros que se han hecho en algún model usamos la función `.objects.all()`, aplicándola al model User está nos devolverá una lista con todos los usuarios registrados, esta se la asignamos a la variable `users` y se la mandamos al html para que la use como `users`

`auth/views.py`
```python
...

class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'auth/users.html', {'users': users})
```
> **Nota:** Los tres puntos (...) Es una referencia de que hay más código en esa posición, el que se hizo anteriormente.

Creamos el archivo `users.html` en la carpeta `templates/auth` , recorremos la variable `users` e imprimimos algunos campos que tiene el modelo `User` (puede consultar los campos que tiene  [aquí](https://docs.djangoproject.com/es/5.0/ref/contrib/auth/) )

`templates/auth/users.html`
```jinja
<style>
    td{
        border: 1px solid black;
        padding: 5px;
    }
</style>
<h1>Lista de Usuarios</h1>
<table>
    <thead>
        <tr>
            <td>ID</td>
            <td>Usuario</td>
            <td>Nombre</td>
            <td>Apellido</td>
            <td>Ultimo login</td>
            <td>Acción</td>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.first_name }}</td>
            <td>{{ user.last_name }}</td>
            <td>{{ user.last_login }}</td>
            <td>
                <a href="#">Editar</a>
                <a href="#">Eliminar</a>
            </td>
        {% endfor %}
    </tbody>
</table>
```
> **Nota:** se usa doble bracket `{{ }}` para imprimir una variable, y bracket porcentaje `{%  %}` para la estructura lógica, como condicionales o ciclos

Añadimos nuestra nueva vista a nuestras rutas

`auth/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("users", views.UsersView.as_view(), name="user-list"), # Nueva Línea
]
```

Ahora vamos a ver que tal nos quedo http://127.0.0.1:8000/users
![UsersList](resources/usuarios_list.png)

### Zona horaria (opcional)

Todo bien hasta aquí, pero...  si eres observador y has hecho la prueba te habrás preguntado, ¿Por qué último login no me muestra una hora distinta a la que en realidad hice el último login?

Esto es por la zona horaria, Django por default usa la zona horaria UTC-0. Podemos o cambiar la zona horaria a la nuestra, o si nuestra aplicación contempla usuarios de varios países cambiar la vista en función de la zona horaria del usuario (avanzado).

Por ahora optaremos por cambiar la zona horaria de django, para esto nos vamos a editar el archivo de configuración

`mi_proyecto/settings.py`

Buscamos el siguiente fragmento de código
```python
TIME_ZONE = 'UTC'
```
y lo reemplazamos con
```python
TIME_ZONE = 'America/Caracas'
```
> **Nota:** No es recomendable hacer esto si tu aplicación contempla usuarios de varios países, o tu país tiene horario de verano. Para más información [accede aquí](https://docs.djangoproject.com/en/5.0/topics/i18n/timezones/)

Actualizamos y listo ya nos muestra la hora según nuestra zona horaria
![UsersList](resources/hora_arreglada.png)

### Haciendo la vista editar

Creamos nuestra clase de editar usuario, en la que según el id que va a estar en el Url vamos a recuperar el modelo usuario, esto con la función get_object_or_404, que indica que si no consigue el modelo según los parámetros que le damos entonces devuelve un 404 (Código http que significa no encontrado).

`auth/views.py`
```python
from django.shortcuts import render, redirect, get_object_or_404 # Añadimos redirect y get_object_or_404
from django.urls import reverse
...


class UserEditView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'auth/user_edit.html', {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        password = request.POST['password']
        if password:
            user.set_password(password) 
        user.save()
        return redirect(reverse('user-list'))
```
> **Nota:** Si no queremos que automáticamente lance el error 404 al no encontrar el usuario, cambiamos el `get_object_or_404(User, id=user_id)` por `User.objects.get(id=user_id)`

Aquí tenemos nuevos conceptos nuevos, el user_id es un parámetro que pasaremos en nuestra ruta, el `redirect` es para redireccionar al usuario a la página que le pases como parámetro, y el `reverse` obtiene la ruta que tenga el nombre que le pases como parámetro (osea la ruta en el `urls.py` que tenga el `name='user-list'`). 

En el post la variable password la ponemos en una condicional, para que si la variable contiene un dato use el método `set_password` para cambiar la contraseña, en cambio si es un texto en blanco ignore la contraseña. Esto recordando que django guarda las contraseñas en forma de un [hash](https://www.redeszone.net/tutoriales/seguridad/criptografia-algoritmos-hash/) y no en texto plano.

Editamos nuestras rutas:

`auth/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("users", views.UsersView.as_view(), name="user-list"), # Al editar el usuario reedireccionará a esta vista
    path("users/edit/<int:user_id>", views.UserEditView.as_view(), name="user-edit"), # Nueva linea, mandando el parámetro numérico(int) user_id a nuestra vista
]
```

y creamos nuestro html

`templates/auth/user_edit.html`
```jinja
<style>
div{
    margin:5px
}
</style>
<h1>Editar Usuario</h1>
<form action="" method="post">
    {% csrf_token %}
    <div>
        <label>
            Usuario
            <input type="text" name="username" value="{{user.username}}">
        </label>
    </div>
    <div>
        <label>
            Contraseña 
            <input type="password" name="password">
            <p> (deja la contraseña en blanco para dejar la misma de antes) </p>
        </label>
    </div>
    <div>
        <label>
            Nombre
            <input type="text" name="first_name" value="{{user.first_name}}">
        </label>
    </div>
    <div>
        <label>
            Apellido
            <input type="text" name="last_name" value="{{user.last_name}}">
        </label>
    </div>
    <button type="submit">Enviar</button>
</form>
```

Ahora para probar nuestra vista vamos a http://127.0.0.1:8000/users/edit/1 recordando que el `1` es el id del usuario. Llenamos los campos como queramos y al guardar nos llevará a nuestra tabla mostrando los campos actualizados. 

### Eliminar

Para esto hacemos una simple vista que obtenga el id del usuario y lo elimine

`auth/views.py`
```python
...


def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect(reverse('user-list'))
```

Añadimos a nuestras rutas

`auth/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("users", views.UsersView.as_view(), name="user-list"),
    path("users/edit/<int:user_id>", views.UserEditView.as_view(), name="user-edit"),
    path("users/delete/<int:user_id>", views.user_delete, name="user-delete"), # Nueva línea
]
```

Y probamos accediendo a http://127.0.0.1:8000/users/delete/1 , este nos debería redirigir a nuestra tabla, quitando el usuario que eliminamos
> **Atención:** No es recomendable eliminar un usuario ya que normalmente se relaciona con otras tablas/modelos. Esto es solo con motivos educacionales

### Repaso

Relación parámetro `name` en los path de los url con el reverse
![SameView1](resources/same_view_5.png)
Relación entre el user_id de la ruta con el parámetro de la vista
![SameView2](resources/same_view_6.png)
Relación de las variables de la vista con las de la plantilla
![SameView3](resources/same_view_7.png)

## Arreglando rutas

Nuestra aplicación va bien, aunque se siente que falta como algo ¿no?. De en vez de escribir en el navegador la ruta que queremos ver, deberíamos agregar unos links en el usuario para poder navegar de mejor forma. ¿Como hacemos esto de la manera Django?

Empezaremos creando un archivo index.html en la carpeta templates/auth , que va a ser nuestras vista inicial que de ahí nos va a reedireccionará al inicio de sesión o al registro.

`templates/auth/index.html`
```jinja
<a href="{% url 'login' %}">Inicio de sesión</a>
<a href="{% url 'register' %}">Registrar Usuario</a>
```
La etiqueta de django `{% url '' %}` en el html hace exactamente lo mismo que la función `reverse` que usamos anteriormente en nuestras vistas. 

Editamos nuestra vista del index para incluir nuestro html que acabamos de crear

`auth/views.py`
```python
...

def index(request):
    return render(request, 'auth/index.html') # Línea Editada
...

```

Guardamos y ahora si accedemos a http://127.0.0.1:8000/ veremos nuestro pequeño menú funcionando.
![Index](resources/index.png).

Ahora necesitamos una función para cerrar sesión, y aparte aprovecharemos para mejorar redirigir al usuario a nuestra tabla cuando inicie sesión

`auth/views.py`
```python
...

from django.contrib.auth import authenticate, login, logout # Añadimos el , logout a esta línea

...

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("user-list")) # Línea Editada
        else:
            return HttpResponse("Credenciales inválidas")

...
# Vista agregada
def logout_view(request):
    logout(request)
    return redirect(reverse("login"))

```
Agregamos nuestra nueva vista a nuestras rutas

`auth/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("users", views.UsersView.as_view(), name="user-list"),
    path("users/edit/<int:user_id>", views.UserEditView.as_view(), name="user-edit"),
    path("users/delete/<int:user_id>", views.user_delete, name="user-delete"), 
    path("logout", views.logout_view, name="logout"), # Línea agregada
]
```

Y ya tenemos nuestra función de cerra sesión hecha, ahora vamos a juntar todo en el html de nuestra tabla

`templates/auth/users.html`
```jinja
<style>
    td{
        border: 1px solid black;
        padding: 5px;
    }
</style>
<a href="{% url 'logout' %}">Cerrar sesión</a>
<h1>Lista de Usuarios</h1>
<table>
    <thead>
        <tr>
            <td>ID</td>
            <td>Usuario</td>
            <td>Nombre</td>
            <td>Apellido</td>
            <td>Ultimo login</td>
            <td>Acción</td>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.first_name }}</td>
            <td>{{ user.last_name }}</td>
            <td>{{ user.last_login }}</td>
            <td>
                <a href="{% url 'user-edit' user.id %}">Editar</a>
                <a href="{% url 'user-delete' user.id %}">Eliminar</a>
            </td>
        {% endfor %}
    </tbody>
</table>
```

Aquí añadimos el enlace para cerrar sesión, además que editamos los enlaces de editar y eliminar para que nos mande a su respectiva vista.

Explicación
`{% url 'user-edit' user.id %}` lo que está dentro de las comillas es el nombre de la ruta en el `urls.py`, y lo que está afuera es los parámetros que pide la ruta. En este caso mandamos el id del usuario.
![Index](resources/url_relation.png).

> **Recomendación:** Como ejercicio puedes agregarle un enlace de volver a editar usuarios, así como colocar una reedirección al registrar un usuario


### Añadiendo algo de seguridad

Como ya hemos visto, cualquiera puede ver, editar y eliminar los usuarios que tenemos, aunque no hayan iniciado sesión igual nuestra aplicación les permite acceder a cualquiera, por eso editaremos nuestras vistas criticas en django para dejar pasar a la gente solo si ha iniciado sesión. Nos quedaría así;

`auth/views.py`
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required # Línea agregada
from django.contrib.auth.mixins import LoginRequiredMixin # Línea agregada

def index(request):
    return render(request, 'auth/login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("user-list"))
        else:
            return HttpResponse("Credenciales inválidas")


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponse("Usuario creado")
    

class UsersView(LoginRequiredMixin, View): # Línea Editada
    def get(self, request):
        users = User.objects.all()
        return render(request, 'auth/users.html', {'users': users})


class UserEditView(LoginRequiredMixin, View): # Línea editada
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'auth/user_edit.html', {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        password = request.POST.get('password')
        if password:
            user.set_password(password) 
        user.save()
        return redirect(reverse('user-list'))


@login_required # Línea agregada
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect(reverse('user-list'))


@login_required # Línea agregada
def logout_view(request):
    logout(request)
    return redirect(reverse("login"))

```

Aquí usamos varios trucos de django para no permitir la entrada a la vista sino ha iniciado sesión, esto a las vistas hechas con una función (ejemplo `def user_delete(request)`) se le añade el decorador `@login_required` justo una línea encima de la función, y en caso de las vistas hechas con clases le ponemos a heredar `LoginRequiredMixin` antes del `View`, por ejemplo `class UserEditView(LoginRequiredMixin, View)` (Tiene que ser antes del `View`, porque al colocarla después no funcionará). Vamos a nuestra página http://127.0.0.1:8000/users, cerramos sesión y tratamos de acceder a la página de users sin haber iniciado a ver que pasa
![Logout Error](resources/logout_error.png).

Nos aparece un error porque django por default nos redirige a la ruta `http://127.0.0.1:8000/accounts/login/`. Ruta que no existe porque no la hemos creado, para arreglar este error configuramos el Django para indicarle cuál es nuestra ruta de inicio de sesión. Editamos el `mi_proyecto/settings.py` y añadimos al final:
```python
...
LOGIN_URL = 'login'
```
(Esto porque en nuestro `urls.py`, nuestra vista de login tiene el name='login')

Ahora cuando intentamos acceder a http://127.0.0.1:8000/users sin haber iniciado sesión nos reedirige al login
