from django.db import models

class cabeceraPro( models.Model ):    
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    

    identificacion = models.CharField(max_length=20)
    nombre = models.CharField(max_length=120)
    fecha_tran = models.DateField()
    numero_fact = models.CharField(max_length=20)
    
    #estado
    #valor_total
    #valor_sin_descuento
    #valor_con_descuento
    
    
    def __str__(self):
        return self.nombre