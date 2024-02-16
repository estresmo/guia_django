from django.urls import path
from . import views

urlpatterns = [
    path("brands", views.view_brands, name="brand-list"),
    path("brands/add", views.add_brand, name="brand-add"),
    path("brands/edit/<int:id>", views.edit_brand, name="brand-edit"),
    path("brands/delete/<int:id>", views.delete_brand, name="brand-delete"),
    path("vehicles", views.VehicleListView.as_view(), name="vehicle-list"),
    path("vehicles/add", views.VehicleAddView.as_view(), name="vehicle-add"),
    path("vehicles/edit/<int:pk>", views.VehicleEditView.as_view(), name="vehicle-edit"),
    path("vehicles/delete/<int:pk>", views.VehicleDeleteView.as_view(), name="vehicle-delete"),
]
