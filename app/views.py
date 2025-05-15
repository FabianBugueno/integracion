from django.shortcuts import render
from .models import Producto
# Create your views here.

def home(request):
    productos = Producto.objects.all()
    data = {'productos': productos}
    return render (request, 'app/home.html', data)

def contacto(request):
    return render (request, 'app/contacto.html')