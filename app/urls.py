from django.urls import path
from .views import home, contacto, agregarProducto, listarProductos, modificarProducto,eliminarProducto
urlpatterns = [
    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path ('agregarProducto/', agregarProducto, name="agregar_Producto"),
    path ('listarProductos/', listarProductos, name="listar_Productos"),
    path ('modificarProducto/<id>', modificarProducto, name="modificar_Producto"),
    path ('eliminarProducto/<id>', eliminarProducto, name="eliminar_Producto" ),
]
