from django.db import models

class cajaUsoManager(models.Manager):
    def get_query_set(self):
        return super(cajaUsoManager, self).get_query_set().filter(estado='O')

class caja ( models.Model ):
    created = models.DateTimeField() 
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100) 
    
    base = models.FloatField()
    totalIngresos = models.FloatField()
    totalEgresos = models.FloatField()
    estado = models.CharField( max_length = 2 )
    saldoCaja = models.FloatField()
    fechaInicio = models.DateField()
    fechaCierre = models.DateField(blank=True, default="")
    
    objects = models.Manager() 
    cajaUso = cajaUsoManager()
           
    

class egreso ( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    
    
    totalEgreso = models.FloatField()    
    fechaEgreso = models.DateField()
    descripcion = models.CharField( max_length=120 )
    cajaId = models.ForeignKey(caja)
    
    class Meta:
        ordering = ['-fechaEgreso']
    
    def save(self):
        super(egreso, self).save()
        actualizarCaja(self, 'E')
    
    
class ingreso ( models.Model ):
    created = models.DateTimeField()
    createdby = models.CharField(max_length=100)
    isactive = models.CharField(max_length=1)
    updated = models.DateTimeField()
    updatedby = models.CharField(max_length=100)    
    
    totalIngreso = models.FloatField()    
    fechaIngreso = models.DateField()
    descripcion = models.CharField( max_length=120 )
    cajaId = models.ForeignKey(caja)  
    
    class Meta:
        ordering = ['-fechaIngreso']
    
    def save(self):
        super(ingreso, self).save()        
        actualizarCaja(self, 'I')
        
    

def actualizarCaja(self, modulo):
        id_caja = self.cajaId.id                  
        obj = caja.objects.get(pk=id_caja)
        if modulo == 'I':
            obj.totalIngresos = float(obj.totalIngresos) + float(self.totalIngreso)
        else:
            obj.totalEgresos = float(obj.totalEgresos) + float(self.totalEgreso)
        obj.save()
        
        
