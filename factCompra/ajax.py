from cliente.models import cliente
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from factCompra.models import cabeceraCompra, productoCompra
from producto.models import producto
import datetime


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


@dajaxice_register
def addProductoCompra( request, cabecera, producto, cantidad, pre_compra, pre_venta, descuento):
    #guardamos el producto    
    prodCompra = productoCompra(created = datetime.datetime.now(),
                                createdby = str(request.user.id),
                                isactive = "Y",
                                updated = datetime.datetime.now(),
                                updatedby = str(request.user.id),                                
                                productoId_id = producto ,  
                                cantidad = cantidad,
                                descuento = descuento,
                                valorTotal = (float(pre_compra) * float(cantidad) - float(descuento)),
                                precioCompra = pre_compra,
                                precioVenta = pre_venta,
                                cabecera_id = cabecera,  )  
    prodCompra.save()
    return listaProductos(cabecera) 
    
    

def listaProductos(cabeceraId):    
    prds = [{ 'id' : i.pk, 
                    'cantidad' : i.cantidad, 
                    'producto' : i.productoId.nombre,
                    'precioCompra' : i.precioCompra,
                    'precioVenta' : i.precioVenta,                    
                    'descuento' : i.descuento,
                    'total' : i.valorTotal, } 
                    for i in productoCompra.objects.filter(cabecera_id=cabeceraId) ]
    return simplejson.dumps({
                            'datos': prds, 
                            })  