from cliente.models import cliente
from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from factVenta.models import cabeceraVenta
from producto.models import producto
import datetime
import json as json




def index(request):      
    #creo una cabecera para la factura    
    cabecera = cabeceraVenta(created = datetime.datetime.now(),
                                createdby = str(request.user.id),
                                isactive = "Y",
                                updated = datetime.datetime.now(),
                                updatedby = str(request.user.id),                                
                                clienteId_id =1,
                                fechaFactura ='1900-01-01',
                                numeroFactura = "0",
                                totalNeto =0,
                                totalDescuento =0,
                                totalPagar =0,
                                estado = "C",
                                formaPago = "N")          
    cabecera.save() 
    cabecera_id = cabecera.id;   
    productos = producto.objects.all();        
    return render_to_response('adminFacturaVenta.html', {"productos": productos, "cabecera":cabecera_id}, 
                              context_instance=RequestContext(request) )

    
    
    