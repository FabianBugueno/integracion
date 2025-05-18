from django import forms
from .models import contacto 

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