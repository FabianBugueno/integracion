from django.shortcuts import render,redirect, get_object_or_404
from .models import Categoria, Producto, Subcategoria
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator 
from django.http import Http404 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from .serializers import ProductoSerializer
import mercadopago
from django.urls import reverse

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer  

    def get_queryset(self):
        productos = Producto.objects.all()
        nombre = self.request.GET.get('nombre')
        if nombre:
            productos = productos.filter(nombre=nombre) 
        return productos

def home(request):
    productos_list = Producto.objects.all()
    paginator = Paginator(productos_list, 8)  # 8 productos por página
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    data = {'productos': productos}
    return render(request, 'app/home.html', data)

def contacto(request):
    data = {
        'form': ContactoForm()
        }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = 'Contacto enviado correctamente!'
        else:
            data['form'] = formulario
    return render (request, 'app/contacto.html',data)
@permission_required('app.add_producto')
def agregarProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto añadido con éxito')
            return redirect('listar_Productos')  # <-- Corrige aquí el nombre
    else:
        form = ProductoForm()
    return render(request, 'app/producto/agregar.html', {'form': form})
@permission_required('app.view_producto')
def listarProductos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try :
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404()
    data = {
        'entity': productos,
        'paginator': paginator 
    }
    return render(request, 'app/producto/listar.html', data)
@permission_required('app.change_producto')
def modificarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto modificado correctamente!')
            return redirect(to="listar_Productos")
        else:
            data['form'] = formulario
    return render(request, 'app/producto/modificar.html', data)
@permission_required('app.delete_producto')
def eliminarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente!')
    return redirect(to="listar_Productos")

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(
                username=formulario.cleaned_data['username'],
                password=formulario.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, 'Usuario registrado correctamente!')
            return redirect(to="home")
        else:
            data['form'] = formulario
    return render(request, 'registration/registro.html', data)
def carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    cantidades = {int(k): v for k, v in carrito.items()}
    total = sum(p.precio * cantidades[p.id] for p in productos)

    # Si el carrito está vacío, solo muestra la página sin preferencia de pago
    if not productos:
        return render(request, 'app/carrito.html', {
            'productos': productos,
            'cantidades': cantidades,
            'total': total,
            'preference_id': None,
            'mp_error': None
        })

    sdk = mercadopago.SDK("TEST-430954136832569-051923-a44ba036140ce3f3f75ca27acaff8d6c-426698245")

    items = []
    for producto in productos:
        items.append({
            "title": producto.nombre,
            "quantity": cantidades[producto.id],
            "unit_price": float(producto.precio),
            "currency_id": "CLP",
        })

    preference_data = {
        "items": items,
        "back_urls": {
            "success": "https://fa31-190-164-158-38.ngrok-free.app/compra/success/",
            "failure": "https://fa31-190-164-158-38.ngrok-free.app/compra/failure/",
            "pending": "https://fa31-190-164-158-38.ngrok-free.app/compra/pending/",
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    print("Preference data:", preference_data)
    print(preference_response)

    preference_id = preference_response["response"].get("id")
    if not preference_id:
        return render(request, 'app/carrito.html', {
            'productos': productos,
            'cantidades': cantidades,
            'total': total,
            'preference_id': None,
            'mp_error': preference_response["response"]
        })

    return render(request, 'app/carrito.html', {
        'productos': productos,
        'cantidades': cantidades,
        'total': total,
        'preference_id': preference_id,
        'mp_error': None
    })

def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    messages.success(request, 'Producto añadido correctamente')
    # Redirige a la página anterior o al home
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def eliminar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('carrito')
@require_POST
def actualizar_carrito(request, producto_id):
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = request.session.get('carrito', {})
    if cantidad > 0:
        carrito[str(producto_id)] = cantidad
    else:
        carrito.pop(str(producto_id), None)
    request.session['carrito'] = carrito
    return redirect('carrito')

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos_list = Producto.objects.filter(categoria=categoria)
    paginator = Paginator(productos_list, 8)  # 8 productos por página
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    return render(request, 'app/productos_por_categoria.html', {
        'categoria': categoria,
        'productos': productos
    })

def productos_por_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    productos = Producto.objects.filter(subcategoria=subcategoria)
    return render(request, 'app/productos_por_categoria.html', {
        'categoria': subcategoria,
        'productos': productos
    })

def compra_exitosa(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    cantidades = {int(k): v for k, v in carrito.items()}
    subtotales = {p.id: p.precio * cantidades[p.id] for p in productos}
    total = sum(p.precio * cantidades[p.id] for p in productos)
    mensaje = "¡Productos comprados exitosamente!"

    # Limpia el carrito solo después de obtener los datos
    request.session['carrito'] = {}

    return render(request, 'app/compra_success.html', {
        'productos': productos,
        'cantidades': cantidades,
        'subtotales': subtotales,
        'total': total,
        'mensaje': mensaje
    })

def compra_fallida(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    cantidades = {int(k): v for k, v in carrito.items()}
    total = sum(p.precio * cantidades[p.id] for p in productos)
    mensaje = "La compra ha fallado. Intenta nuevamente."
    return render(request, 'app/compra_failure.html', {
        'productos': productos,
        'cantidades': cantidades,
        'total': total,
        'mensaje': mensaje
    })

def compra_pendiente(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    cantidades = {int(k): v for k, v in carrito.items()}
    total = sum(p.precio * cantidades[p.id] for p in productos)
    mensaje = "La compra está pendiente de confirmación."
    return render(request, 'app/compra_pending.html', {
        'productos': productos,
        'cantidades': cantidades,
        'total': total,
        'mensaje': mensaje
    })

def buscar_productos(request):
    query = request.GET.get('q', '')
    productos_list = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.none()
    paginator = Paginator(productos_list, 8)  # 8 productos por página
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    return render(request, 'app/busqueda.html', {
        'productos': productos,
        'query': query,
    })

