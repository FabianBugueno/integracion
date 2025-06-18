from django.contrib import admin
from .models import Marca, Categoria, Subcategoria, Producto, contacto 
from .forms import ProductoForm
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):  
    list_display = ('nombre', 'precio', 'nuevo', 'marca', 'stock')
    list_editable = ('precio', 'stock')
    search_fields = ('nombre',)
    list_filter = ('nuevo', 'marca')
    form = ProductoForm

admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Subcategoria)  # <-- Agrega esta línea
admin.site.register(Producto, ProductoAdmin)   
admin.site.register(contacto)