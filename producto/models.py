from django.core.exceptions import ValidationError
from django.db import models

class producto( models.Model ):    
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    

    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=120)
    cantidad = models.FloatField()
    preciocompra = models.FloatField()
    precioventa = models.FloatField()
    imagen = models.CharField(max_length=200, blank=True, null=True)
    descuento_max = models.FloatField()
    observaciones = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        if self.precioventa <= self.preciocompra:
            raise ValidationError('El precio de venta debe ser mayor que el precio de compra',)
            
        
        if self.pk == None:
            if producto.objects.filter(codigo=self.codigo).exists():
                raise ValidationError('Ya existe un producto con este codigo.')
