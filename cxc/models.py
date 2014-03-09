from django.db import models

from factVenta.models import cabeceraVenta
from cliente.models import cliente

class cabeceraCxc ( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100) 
    
    totalAbonosGeneral = models.FloatField()
    totalDeudaGeneral = models.FloatField()     
    clienteId = models.ForeignKey(cliente)   


class cuentaCobrar ( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100) 
    
    totalAbonos = models.FloatField()
    totalDeuda = models.FloatField()
    facturaId = models.ForeignKey(cabeceraVenta)
    cabeceraId = models.ForeignKey(cabeceraCxc)
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
    cuentaId = models.ForeignKey(cabeceraCxc)