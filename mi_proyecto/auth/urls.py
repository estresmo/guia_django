from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("users", views.UsersView.as_view(), name="user-list"),
    path("users/edit/<int:user_id>", views.UserEditView.as_view(), name="user-edit"),
    path("users/delete/<int:user_id>", views.user_delete, name="user-delete"), 
]
