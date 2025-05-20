from django.urls import path, include
from .views import home, contacto, agregarProducto, \
    listarProductos, modificarProducto,eliminarProducto, \
    registro, ProductoViewSet
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)



urlpatterns = [
    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path ('agregarProducto/', agregarProducto, name="agregar_Producto"),
    path ('listarProductos/', views.listarProductos, name='listar_Productos'),  # <-- El nombre debe ser listar_Productos
    path ('modificarProducto/<id>', modificarProducto, name="modificar_Producto"),
    path ('eliminarProducto/<int:id>/', eliminarProducto, name="eliminar_Producto" ),
    path ('registro/', registro, name="registro" ),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar_carrito/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('actualizar_carrito/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('subcategoria/<int:subcategoria_id>/', views.productos_por_subcategoria, name='productos_por_subcategoria'),  # <-- Agrega esta línea
    path('api/productos/', include(router.urls)), 
]
