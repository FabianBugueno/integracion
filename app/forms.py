from django import forms
from .models import contacto, Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator
from django.forms import ValidationError

class ContactoForm(forms.ModelForm):
    class Meta:
        model = contacto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_consulta': forms.Select(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
            'avisos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class ProductoForm(forms.ModelForm):
    imagen = forms.ImageField(required=False, validators=[MaxSizeFileValidator(max_size=5)])
    nombre = forms.CharField(min_length=3, max_length=50)
    precio = forms.IntegerField(min_value=1)
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        existe = Producto.objects.filter(nombre__iexact=nombre).exists()
        if existe:
            raise ValidationError('El nombre del producto ya existe')   
        return nombre   

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            "fecha_fabricacion": forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fecha_fabricacion'].initial = self.instance.fecha_fabricacion.strftime('%Y-%m-%d')

class CustomUserCreationForm(UserCreationForm):
    class Meta:  
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
