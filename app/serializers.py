from .models import Producto, Marca
from rest_framework import serializers

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'  

class ProductoSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.CharField(source='marca.nombre', read_only=True)
    marca = MarcaSerializer(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(),
        source='marca'
    )
    nombre = serializers.CharField(required=True, min_length= 3 ,max_length=50)

    def validate_nombre(self, value):
        existe = Producto.objects.filter(nombre__iexact=value).exists()
        if existe:
            raise serializers.ValidationError("El nombre del producto ya existe")
        return value

    class Meta:
        model = Producto
        fields = '__all__'  