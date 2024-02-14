from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
    

class UsersView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'auth/users.html', {'users': users})


class UserEditView(LoginRequiredMixin, View):
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


@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect(reverse('user-list'))


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("login"))
