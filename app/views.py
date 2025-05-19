from django.shortcuts import render,redirect, get_object_or_404
from .models import Producto
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator 
from django.http import Http404 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST

def home(request):
    productos = Producto.objects.all()
    data = {'productos': productos}
    return render (request, 'app/home.html', data)

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
    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = 'Producto agregado correctamente!'
        else:
            data['form'] = formulario
    return render(request, 'app/producto/agregar.html', data)
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
    return render(request, 'app/carrito.html', {
        'productos': productos,
        'cantidades': cantidades,
        'total': total,
    })

def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect('carrito')

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