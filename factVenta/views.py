from cliente.models import cliente
from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from factVenta.models import cabeceraVenta, armarCadena
from producto.models import producto
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
    

def imprimirFact(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=primer.pdf' 
    c = canvas.Canvas(response, pagesize=letter) 
    c.roundRect(45,650,250,100,20,stroke=1, fill=0)
    c.roundRect(310,650,250,100,20,stroke=1, fill=0)
    c.roundRect(45,150,510,480,20,stroke=1, fill=0)
    x = 50
    y = 600
    for i in range(300):
        c.drawString(x, y, 'esto')        
        y = y - 10
        
        
    c.showPage()
    c.save()
    return response


    
    
    