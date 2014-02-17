from django.db import models

from factVenta.models import cabeceraVenta 

class cuentaCobrar ( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100) 
    
    totalAbonos = models.FloatField()
    caberaId = models.ForeignKey()