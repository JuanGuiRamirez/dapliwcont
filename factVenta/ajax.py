from cliente.models import cliente
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db.models.aggregates import Sum
from django.utils import simplejson
from factVenta.models import productoVenta, cabeceraVenta
from producto.models import producto
import datetime


@dajaxice_register
def getProductos(request, codigoPrd, cabeceraId):
    if codigoPrd:
        productoajax = producto.objects.filter(codigo=codigoPrd)[:1] 
        countProductos = productoVenta.objects.filter(cabecera_id=cabeceraId).filter(productoId_id = productoajax[0].id)[:1]
        if countProductos:
            countProductos[0].cantidad = countProductos[0].cantidad  + 1
            countProductos[0].valorTotal = countProductos[0].valorTotal  + productoajax[0].precioventa
            countProductos[0].save()        
        else:
            productoxVenta = productoVenta(created = datetime.datetime.now(),
                                    createdby = 1,
                                    isactive = "Y",
                                    updated = datetime.datetime.now(),
                                    updatedby = 1,  
                                    productoId_id = productoajax[0].id,
                                    nombreProducto = productoajax[0].nombre,
                                    cantidad = 1,
                                    descuento = 0,
                                    valorTotal = productoajax[0].precioventa, 
                                    cabecera_id =  cabeceraId)   
            productoxVenta.save()   
                 
        return listaProductos(cabeceraId)
    
    
    
@dajaxice_register
def getClientes(request, nitCliente, fechaFact, numFact, cabeceraId ):
    actualizaCabecera(nitCliente, fechaFact, numFact, cabeceraId, 'N', '')
    clientAjax = cliente.objects.filter(identificacion=nitCliente)[:1]       
    return simplejson.dumps({
                              'tercero': clientAjax[0].nombre,
                              'identificacion' : clientAjax[0].identificacion,                               
                              }) 
    
def actualizaCabecera( nitCliente, fechaFact, numFact, cabeceraId, forPago, est ):
    cabecera = cabeceraVenta.objects.get(pk=cabeceraId)
    if nitCliente:
        clientAjax = cliente.objects.filter(identificacion=nitCliente)[:1]
        cabecera.clienteId_id = clientAjax[0].id
    if fechaFact:
        cabecera.fechaFactura = fechaFact
    if numFact:
        cabecera.numeroFactura = numFact 
    if est:
        cabecera.estado = est 
    cabecera.formaPago = forPago  
    cabecera.save()       


def calcularTotales (cabeceraId):
    cabecera = cabeceraVenta.objects.get(pk=cabeceraId)
    total_pagar = productoVenta.objects.filter(cabecera_id=cabeceraId).aggregate(Sum('valorTotal'), Sum('descuento'))
    if total_pagar["valorTotal__sum"] == None:
        total_pagar["valorTotal__sum"] = 0
    if total_pagar["descuento__sum"] == None:
        total_pagar["descuento__sum"] = 0 
    cabecera.totalNeto = total_pagar["valorTotal__sum"] 
    cabecera.totalDescuento = total_pagar["descuento__sum"]
    cabecera.totalPagar = total_pagar["valorTotal__sum"] - total_pagar["descuento__sum"]       
    cabecera.save()   
    


@dajaxice_register
def eliminarPrd (request, numPrd, cabeceraId):
    prdEliminar = productoVenta.objects.filter(pk=numPrd)
    prdEliminar.delete()
    return listaProductos(cabeceraId)



@dajaxice_register
def cargarEdit(request, numPrd):
    dajax = Dajax()
    prdEditar = productoVenta.objects.filter(pk=numPrd)
    dajax.assign('#txtNombrePrd','value',str(prdEditar[0].nombreProducto))
    dajax.assign('#txtCantidadPrd','value',str(prdEditar[0].cantidad))
    dajax.assign('#txtDescuentoPrd','value',str(prdEditar[0].descuento))
    dajax.assign('#txtProductoCargado','value',str(prdEditar[0].id))
    return dajax.json()


@dajaxice_register
def adicionarEdit(request, numPrd, cant, desc, cabeceraId):    
    prdEditar = productoVenta.objects.get(pk=numPrd)
    prd = producto.objects.filter(pk = prdEditar.productoId_id)
    prdEditar.cantidad = float(cant)
    prdEditar.descuento = float(desc)
    prdEditar.valorTotal = ((prd[0].precioventa * float(cant)) - float(desc))
    prdEditar.save()    
    return listaProductos(cabeceraId) 


def listaProductos(cabeceraId):
    
    calcularTotales(cabeceraId)
    cabecera = cabeceraVenta.objects.get(pk=cabeceraId)
    
    prds = [{ 'id' : i.pk, 
                    'cantidad' : i.cantidad, 
                    'nombrePrd' : i.nombreProducto,
                    'descuento' : i.descuento,
                    'total' : i.valorTotal, } 
                    for i in productoVenta.objects.filter(cabecera_id=cabeceraId) ]        
        
                 
    return simplejson.dumps({
                            'datos': prds,
                            'mensaje' : 'DIOS es grande!',
                            'neto' : cabecera.totalNeto,
                            'descuento' : cabecera.totalDescuento,
                            'total' : cabecera.totalPagar
                            })        
    

@dajaxice_register
def facturar (request, cabeceraId, formaPago, fechaFact, numFact):
    #actualizamos el inventario
    for i in productoVenta.objects.filter(cabecera_id=cabeceraId):
        prdEdit = producto.objects.get(pk=i.productoId_id)
        prdEdit.cantidad = prdEdit.cantidad - i.cantidad
        prdEdit.save()
    
    #actualizamos cabecera
    actualizaCabecera('', fechaFact, numFact, cabeceraId, formaPago, 'F')
    
    #falta crear cxp o cxc
    