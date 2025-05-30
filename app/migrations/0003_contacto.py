# Generated by Django 5.0.4 on 2025-05-17 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_producto_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('tipo_consulta', models.IntegerField(choices=[(0, 'Consulta'), (1, 'Reclamo'), (2, 'Sugerencia'), (3, 'Otro')])),
                ('mensaje', models.TextField()),
                ('avisos', models.BooleanField()),
            ],
        ),
    ]
