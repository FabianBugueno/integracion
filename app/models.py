from django.db import models

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField
    nuevo = models.BooleanField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_fabricacion = models.DateField()
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
opciones_consulta = [
    [0, 'Consulta'],
    [1, 'Reclamo'],
    [2, 'Sugerencia'],
    [3, 'Otro']
]
class contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta)
    mensaje = models.TextField()
    avisos = models.BooleanField()
    
    def __str__(self):
        return self.nombre