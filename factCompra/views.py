from django.shortcuts import render_to_response
from django.template.context import RequestContext
from factCompra.models import cabeceraCompra
import datetime




def index(request):       
    #creo una cabecera para la factura    
    cabecera = cabeceraCompra(created = datetime.datetime.now(),
                                createdby = str(request.user.id),
                                isactive = "Y",
                                updated = datetime.datetime.now(),
                                updatedby = str(request.user.id),                                
                                proveedorId_id =1,
                                fechaFactura ='1900-01-01',
                                numeroFactura = 0,
                                totalNeto =0,
                                totalDescuento = 0,
                                totalPagar = 0,
                                estado = "C",
                                formaPago = "N")          
    cabecera.save() 
    cabecera_id = cabecera.id;           
    return render_to_response('adminFacturaCompra.html', {"cabecera":cabecera_id,}, 
                              context_instance=RequestContext(request) )
    