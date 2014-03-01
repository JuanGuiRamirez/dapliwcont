from caja.models import caja, ingreso, egreso
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from datetime import date
import datetime


@dajaxice_register
def registroMvt(request, monto, fecha, observacion, modulo):
    cajaOpen = caja.cajaUso.all()    
    if modulo == 'I':
        obj = ingreso(
                        totalIngreso = monto,    
                        fechaIngreso = fecha,
                        created = datetime.datetime.now(),
                        createdby = str(request.user.id),
                        isactive = "Y",
                        updated = datetime.datetime.now(),
                        updatedby = str(request.user.id),
                        descripcion = observacion,
                        cajaId_id = cajaOpen[0].id   )
    else:
        obj = egreso(
                        totalEgreso = monto,    
                        fechaEgreso = fecha,
                        created = datetime.datetime.now(),
                        createdby = str(request.user.id),
                        isactive = "Y",
                        updated = datetime.datetime.now(),
                        updatedby = str(request.user.id),
                        descripcion = observacion,
                        cajaId_id = cajaOpen[0].id   )
        
    
    
    obj.save()
    return listaMvt(modulo, cajaOpen[0].id) 
    
    


def listaMvt(mod, caja):
    
    if mod == 'I':
        prds = [{   'id' : i.pk, 
                    'fecha' : str(i.fechaIngreso), 
                    'valor' : i.totalIngreso,} 
                    for i in ingreso.objects.filter(cajaId_id=caja) ] 
    else:
        prds = [{   'id' : i.pk, 
                    'fecha' : i.fechaEgreso, 
                    'valor' : i.totalEgreso,} 
                    for i in ingreso.objects.filter(cajaId_id=caja) ] 
           
        
                 
    return simplejson.dumps({
                            'datos': prds,
                            }) 


    