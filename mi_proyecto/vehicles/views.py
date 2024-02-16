from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .models import Brand, Vehicle
from .forms import BrandForm, VehicleForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def view_brands(request):
    brands = Brand.objects.all()
    context = {'brands': brands}
    return render(request, 'vehicles/brands.html', context)

def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("brand-list"))
    else:
        form = BrandForm()
    context = {'form': form}
    return render(request, 'vehicles/add_brand.html', context)

def edit_brand(request, id):
    brand = Brand.objects.get(id=id)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect(reverse("brand-list"))
    else:
        form = BrandForm(instance=brand)
    context = {'form': form}
    return render(request, 'vehicles/add_brand.html', context)


def delete_brand(request, id):
    brand = Brand.objects.get(id=id)
    brand.delete()
    return redirect(reverse("brand-list"))


class VehicleListView(ListView):
    model = Vehicle


class VehicleAddView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    success_url = reverse_lazy("vehicle-list")


class VehicleEditView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    success_url = reverse_lazy("vehicle-list")


class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicle-list")
