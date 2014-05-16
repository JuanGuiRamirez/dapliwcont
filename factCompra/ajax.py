from cliente.models import cliente
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db.models.aggregates import Sum
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
    prdEditar = productoCompra.objects.filter(productoId_id = producto, isactive = 'Y', cabecera_id = cabecera)    
    if prdEditar:
        prdEditar[0].cantidad = cantidad
        prdEditar[0].descuento = descuento
        prdEditar[0].precioCompra = pre_compra
        prdEditar[0].precioVenta = pre_venta
        prdEditar[0].valorTotal = (float(pre_compra) * float(cantidad) - float(descuento))
        prdEditar[0].valorNeto = (float(pre_compra) * float(cantidad) )
        prdEditar[0].save()
    else:    
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
                                    cabecera_id = cabecera,
                                    valorNeto =  (float(pre_compra) * float(cantidad)), )  
        prodCompra.save()
    return listaProductos(cabecera) 
    

@dajaxice_register
def cargarEdit(request, numPrd):
    dajax = Dajax()
    prdEditar = productoCompra.objects.filter(pk=numPrd)    
    dajax.assign('#txtNombrePrd','value',str(prdEditar[0].productoId))
    dajax.assign('#txtProductoCargado','value',str(prdEditar[0].productoId_id))    
    dajax.assign('#txtCantidadPrd','value', prdEditar[0].cantidad)
    dajax.assign('#txtPrecioC','value', prdEditar[0].precioCompra)
    dajax.assign('#txtPrecioV','value', prdEditar[0].precioVenta)
    dajax.assign('#txtDescuentoPrd','value', prdEditar[0].descuento)
    return dajax.json()


def calcularTotales (cabeceraId):
    cabecera = cabeceraCompra.objects.get(pk=cabeceraId)
    total_pagar = productoCompra.objects.filter(cabecera_id=cabeceraId).aggregate(Sum('valorNeto'), Sum('descuento'))
    if total_pagar["valorNeto__sum"] == None:
        total_pagar["valorNeto__sum"] = 0
    if total_pagar["descuento__sum"] == None:
        total_pagar["descuento__sum"] = 0 
    cabecera.totalNeto = total_pagar["valorNeto__sum"] 
    cabecera.totalDescuento = total_pagar["descuento__sum"]
    cabecera.totalPagar = total_pagar["valorNeto__sum"] - total_pagar["descuento__sum"]       
    cabecera.save()   
    

@dajaxice_register
def eliminarPrd (request, numPrd, cabeceraId):
    prdEliminar = productoCompra.objects.filter(pk=numPrd)
    prdEliminar.delete()
    return listaProductos(cabeceraId)
    

def listaProductos(cabeceraId):
    
    calcularTotales(cabeceraId)
    cabecera = cabeceraCompra.objects.get(pk=cabeceraId)
        
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
                            'total': cabecera.totalNeto,
                            'desc': cabecera.totalDescuento,
                            'totalPagar': cabecera.totalPagar, 
                            })  
    
    
    