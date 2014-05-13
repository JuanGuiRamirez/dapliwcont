from cliente.models import cliente
from django.db import models
from producto.models import producto

class cabeceraCompra( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    

    proveedorId = models.ForeignKey(cliente)
    fechaFactura = models.DateField()
    numeroFactura = models.CharField(max_length=20)
    totalNeto = models.FloatField()
    totalDescuento = models.FloatField()
    totalPagar = models.FloatField()
    estado = models.CharField(max_length=1)
    formaPago = models.CharField(max_length=1)
    
    def __str__(self):
        self.numeroFactura
        

class productoCompra( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    

    productoId = models.ForeignKey(producto)      
    cantidad = models.FloatField()
    descuento = models.FloatField()
    valorTotal = models.FloatField()
    precioCompra = models.FloatField()
    precioVenta = models.FloatField()
    cabecera = models.ForeignKey(cabeceraCompra)
    
    def __str__(self):
        self.productoId