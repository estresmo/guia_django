from django.db import models


class Brand(models.Model):
    class Meta:
        verbose_name = "marca"

    name = models.CharField(max_length=100, unique=True, verbose_name="nombre")

    def __str__(self) :
        return self.name


class Vehicle(models.Model):
    class Type(models.IntegerChoices):
        MOTO = 1, "Moto"
        CAR = 2, "Carro"
        TRUCK = 3, "Camión"

    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)  # Marca
    year = models.IntegerField() # Año
    photo = models.FileField(upload_to="vehicles") # Foto
    type = models.IntegerField(choices=Type.choices)   # Tipo de vehículo
    model = models.CharField(max_length=100, unique=True)  # Modelo del vehículo
    price = models.IntegerField() # Precio
    created_at = models.DateTimeField(auto_now_add=True) # Fecha de creación

    def __str__(self) :
        return self.brand.name + self.model
    
    def type_label(self):
        return self.Type(self.type).label