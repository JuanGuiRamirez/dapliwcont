from django.core.exceptions import ValidationError
from django.db import models

class cliente( models.Model ):    
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    

    identificacion = models.CharField(max_length=20)
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    telefono = models.CharField(max_length=120)
    celular = models.CharField(max_length=120)
    saldodeuda = models.FloatField()
    saldofavor = models.FloatField()
    limitecredito = models.FloatField()
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        if cliente.objects.filter(identificacion=self.identificacion).exists():
            raise ValidationError('Ya existe un tercero con este numero de identificacion.')
            
        
