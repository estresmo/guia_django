from django.forms import ModelForm
from .models import Brand, Vehicle

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class VehicleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vehicle
        exclude = ['created_at']