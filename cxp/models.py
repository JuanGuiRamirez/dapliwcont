from cliente.models import cliente
from django.db import models
from factCompra.models import cabeceraCompra


class cabeceraCxp ( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100) 
    
    totalAbonosGeneral = models.FloatField()
    totalDeudaGeneral = models.FloatField()     
    proveedorId = models.ForeignKey(cliente) 
    

class cuentaPagar( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100) 
    
    totalAbonos = models.FloatField()
    totalDeuda = models.FloatField()
    facturaId = models.ForeignKey(cabeceraCompra)
    cabeceraId = models.ForeignKey(cabeceraCxp)
    fechaCuenta = models.DateField()
    
    

class abono ( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)     
    
    fechaAbono = models.DateField()
    montoAbono = models.FloatField()
    saldoInicial = models.FloatField()
    saldoFinal = models.FloatField()
    cuentaId = models.ForeignKey(cabeceraCxp)