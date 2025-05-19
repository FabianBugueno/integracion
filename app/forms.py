from django import forms
from .models import contacto, Producto, Categoria, Subcategoria
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator
from django.forms import ValidationError, DateInput
from django.contrib import messages

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
    categoria_subcategoria = forms.ChoiceField(label="Categoría", choices=[])

    class Meta:
        model = Producto
        exclude = []
        widgets = {
            'fecha_fabricacion': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordena los campos como desees
        field_order = [
            'nombre',
            'precio',
            'descripcion',
            'nuevo',
            'marca',
            'categoria_subcategoria',  # <-- Aquí antes de fecha_fabricacion
            'fecha_fabricacion',
            'imagen',
        ]
        # Solo incluye los campos que existen en el formulario
        self.order_fields([f for f in field_order if f in self.fields])

        choices = []
        for categoria in Categoria.objects.all():
            choices.append((f"cat_{categoria.id}", f"{categoria.nombre}"))
            for sub in Subcategoria.objects.filter(categoria=categoria):
                choices.append((f"sub_{sub.id}", f"— {sub.nombre}"))
        self.fields['categoria_subcategoria'].choices = choices

        self.fields['categoria'].widget = forms.HiddenInput()
        self.fields['subcategoria'].widget = forms.HiddenInput()

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Si el formulario tiene instancia (es edición), exclúyela de la búsqueda
        qs = Producto.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('El nombre del producto ya existe')   
        return nombre   

    def clean(self):
        cleaned_data = super().clean()
        seleccion = cleaned_data.get('categoria_subcategoria')
        if seleccion:
            if seleccion.startswith('cat_'):
                cat_id = int(seleccion.replace('cat_', ''))
                cleaned_data['categoria'] = Categoria.objects.get(id=cat_id)
                cleaned_data['subcategoria'] = None
            elif seleccion.startswith('sub_'):
                sub_id = int(seleccion.replace('sub_', ''))
                sub = Subcategoria.objects.get(id=sub_id)
                cleaned_data['categoria'] = sub.categoria
                cleaned_data['subcategoria'] = sub
        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:  
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

form = ProductoForm

def agregar_carrito(request, producto_id):
    # ...tu lógica para agregar al carrito...
    messages.success(request, 'Producto añadido correctamente')
    return redirect('home')  # O la vista que corresponda
