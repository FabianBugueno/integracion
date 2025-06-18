from django.urls import path, include
from .views import home, contacto, agregarProducto, \
    listarProductos, modificarProducto,eliminarProducto, \
    registro, ProductoViewSet
from rest_framework.routers import DefaultRouter
from . import views
from django import template

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key, '')

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
    path('compra/success/', views.compra_exitosa, name='compra_success'),
    path('compra/failure/', views.compra_fallida, name='compra_failure'),
    path('compra/pending/', views.compra_pendiente, name='compra_pending'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('mis-compras/', views.mis_compras, name='mis_compras'),
    path('nosotros/', views.nosotros, name='nosotros'),   path('nosotros/', views.nosotros, name='nosotros'),
    path('cliente/', views.vista_cliente, name='vista_cliente'),
    path('vendedor/', views.vista_vendedor, name='vista_vendedor'),
    path('bodeguero/', views.vista_bodeguero, name='vista_bodeguero'),
    path('vendedor/aprobar/<int:pedido_id>/', views.aprobar_pedido, name='aprobar_pedido'),
    path('vendedor/rechazar/<int:pedido_id>/', views.rechazar_pedido, name='rechazar_pedido'),
    path('bodeguero/listo/<int:pedido_id>/', views.marcar_listo, name='marcar_listo'),
]

