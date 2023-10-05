from django.db import models


class Cliente(models.Model):
    nro_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    activo = models.BooleanField()

    class Meta:
        db_table = 'e01_cliente'


class DetalleFactura(models.Model):
    # The composite primary key (nro_factura, codigo_producto) found, that is not supported. id column is added.
    id = models.AutoField(primary_key=True)
    nro_factura = models.ForeignKey('Factura', models.DO_NOTHING, db_column='nro_factura')
    codigo_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='codigo_producto')
    nro_item = models.IntegerField()
    cantidad = models.FloatField()

    class Meta:
        db_table = 'e01_detalle_factura'
        unique_together = (('nro_factura', 'codigo_producto'),)


class Factura(models.Model):
    nro_factura = models.AutoField(primary_key=True)
    fecha = models.DateField()
    total_sin_iva = models.FloatField()
    iva = models.FloatField()
    total_con_iva = models.FloatField(blank=True, null=True)
    nro_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='nro_cliente')

    class Meta:
        db_table = 'e01_factura'


class Producto(models.Model):
    codigo_producto = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=45)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    precio = models.FloatField()
    stock = models.IntegerField()

    class Meta:
        db_table = 'e01_producto'


class Telefono(models.Model):
    # The composite primary key (codigo_area, nro_telefono) found, that is not supported. id column is added.
    id = models.AutoField(primary_key=True)
    codigo_area = models.IntegerField()
    nro_telefono = models.IntegerField()
    tipo = models.CharField(max_length=1)
    nro_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='nro_cliente')

    class Meta:
        db_table = 'e01_telefono'
        unique_together = (('codigo_area', 'nro_telefono'),)
