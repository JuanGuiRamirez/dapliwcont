from django.db import models
from cliente.models import cliente
from producto.models import producto


class cabeceraVenta( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    

    clienteId = models.ForeignKey(cliente)
    fechaFactura = models.DateField()
    numeroFactura = models.CharField(max_length=20)
    totalNeto = models.FloatField()
    totalDescuento = models.FloatField()
    totalPagar = models.FloatField()
    estado = models.CharField(max_length=1)
    formaPago = models.CharField(max_length=1)
    
    def __str__(self):
        self.numeroFactura


class productoVenta( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    

    productoId = models.ForeignKey(producto)
    nombreProducto = models.CharField(max_length=120)    
    cantidad = models.FloatField()
    descuento = models.FloatField()
    valorTotal = models.FloatField()
    cabecera = models.ForeignKey(cabeceraVenta)
    
    def __str__(self):
        self.productoId
        

def armarCadena():
    pass
