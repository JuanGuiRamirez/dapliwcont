from cliente.models import cliente
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from factCompra.models import cabeceraCompra
from producto.models import producto


@dajaxice_register
def cargarProv( request, nitProv, cabecera ):
    dajax = Dajax()
    prov = cliente.objects.filter(identificacion=nitProv, isactive='Y')
    if prov:
        dajax.assign('#txtNombreProveedor','value',str(prov[0]))
        cabecera = cabeceraCompra.objects.get(pk=cabecera)
        cabecera.proveedorId = prov[0]
        cabecera.save()
    else:
        dajax.assign('#txtNombreProveedor','value','')        
    return dajax.json()

@dajaxice_register
def cargarProducto( request, nitProducto ):
    dajax = Dajax()
    prod = producto.objects.filter(codigo=nitProducto, isactive='Y')
    if prod:
        dajax.assign('#txtNombrePrd','value',str(prod[0]))
        dajax.assign('#txtProductoCargado','value',str(prod[0].id))
    else:
        dajax.assign('#txtNombrePrd','value','')  
        dajax.assign('#txtProductoCargado','value',str(0))      
    return dajax.json()