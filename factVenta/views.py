from cliente.models import cliente
from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from factVenta.models import cabeceraVenta
from producto.models import producto
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import json as json




def index(request):    
    consecutivo = consecutivoFact()  
    #creo una cabecera para la factura    
    cabecera = cabeceraVenta(created = datetime.datetime.now(),
                                createdby = str(request.user.id),
                                isactive = "Y",
                                updated = datetime.datetime.now(),
                                updatedby = str(request.user.id),                                
                                clienteId_id =1,
                                fechaFactura ='1900-01-01',
                                numeroFactura = consecutivo,
                                totalNeto =0,
                                totalDescuento =0,
                                totalPagar =0,
                                estado = "C",
                                formaPago = "N")          
    cabecera.save() 
    cabecera_id = cabecera.id;   
    productos = producto.objects.all();        
    return render_to_response('adminFacturaVenta.html', {"productos": productos, "cabecera":cabecera_id, "numFactura":consecutivo}, 
                              context_instance=RequestContext(request) )
    

def consecutivoFact():
    registros = cabeceraVenta.objects.filter(estado='F').count() + 1
    cadena = ''
    for i in range(10-len(str(registros))):
        cadena += '0'
    cadena += str(registros)
    return cadena
        

def imprimirFact(request, cabecera):
    
    factura = cabeceraVenta.objects.get(pk=cabecera)
    forma = ''
    
    if factura.formaPago == 'F':
        forma = 'Credito'
    else:
        forma = 'Contado'   
        
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=primer.pdf' 
    c = canvas.Canvas(response) 
    
    
    #fuente para el titulo
    c.setFont("Helvetica", 24) 
    c.drawString(120, 800, 'DAPLIW') 
    c.setFont("Helvetica", 16)
    c.drawString(120, 780, 'Nit: 890465322')
    c.drawString(350, 805, 'Factura de venta')
    c.setFont("Helvetica", 14)
    c.drawString(350, 785, 'Nro: ' + str(factura.numeroFactura))

    c.roundRect(45,680,250,70,20,stroke=1, fill=0)
    c.setFont("Helvetica", 9)
    c.drawString(60, 730, 'Cliente: ' + str(factura.clienteId))
    c.drawString(60, 715, 'Identificacion: ' + str(factura.clienteId.identificacion))

    c.roundRect(310,680,250,70,20,stroke=1, fill=0)
    c.drawString(325, 730, 'Fecha Factura: ' + str(factura.fechaFactura))
    c.drawString(325, 715, 'Numero Factura: ' + str(factura.numeroFactura))
    c.drawString(325, 700, 'Forma de Pago: ' + forma)

    c.roundRect(45,250,515,420,20,stroke=1, fill=0)
    c.drawString(63, 650, 'Cantidad')
    c.drawString(190, 650, 'Descripcion')
    c.drawString(330, 650, 'Precio Unit.')
    c.drawString(420, 650, 'Descuento')
    c.drawString(505, 650, 'Total')

    c.line(120,670,120,250)
    c.line(310,670,310,250)
    c.line(400,670,400,250)
    c.line(480,670,480,250)
    c.line(45,640,560,640) #horizontal

    c.roundRect(45,160,340,80,20,stroke=1, fill=0)
    c.roundRect(395,160,170,80,20,stroke=1, fill=0)
    c.drawString(55, 225, 'Observaciones: ')

    c.drawString(405, 220, 'Subtotal: ')
    c.drawString(405, 195, 'Descuento: ')
    c.drawString(405, 170, 'Total: ')

    c.line(395,210,565,210)
    c.line(395,185,565,185)
    c.line(480,160,480,240)
    
    c.drawString(490, 220, str(factura.totalNeto))
    c.drawString(490, 195, str(factura.totalDescuento))
    c.drawString(490, 170, str(factura.totalPagar))

    c.roundRect(45,65,140,85,20,stroke=1, fill=0)
    c.roundRect(425,65,140,85,20,stroke=1, fill=0) 
    
    c.setFont("Helvetica", 8)
    c.line(430,83,560,83)
    c.drawString(57, 70, 'FIRMA Y SELLO AUTORIZADO')
    c.drawString(433, 137, 'ACEPTADO') 
    c.drawString(450, 70, 'NOMBRE Y C.C O N.I.T')  
    
    
    c.setFont("Helvetica", 9)
    x = 50
    y = 625
    for i in range(31):
        c.drawString(x, y, 'esto' + str(i)) 
        c.drawString(130, y, 'descripcion bien larga para ver como') 
        c.drawString(320, y, '1000000' + str(i)) 
        c.drawString(410, y, '1000000' + str(i)) 
        c.drawString(490, y, '1000000' + str(i))        
        y = y - 12
        if str(i) == '44':
            c.showPage() 
            
    texto = """Nota: 1. La presente factura de venta se asimila
            en todos sus efectos a la letra de cambio. 2. En
            caso de mora se causara el interes autorizado
            por la ley. 3. Se hace constar que la firma de una
            persona distinta del comprador implica que dicha
            persona esta autorizada expresamente por el
            comprador para firmar, confiar la deuda y obligar
            al comprador. 4. Recibi de conformidad la
            mercancia o servicio que le trata esta factura y
            acepto el valor estipulado en la misma."""

    


    textobject = c.beginText()  # Iniciamos el textobject
    textobject.setTextOrigin(190, 140)  # Ubicamos el cursor donde dibujar
    textobject.setCharSpace(0.5)  # Espacio entre caracteres 
    textobject.setWordSpace(1)  # Espacio entre palabras    
    textobject.setLeading(8)  # Espaciado entre lineas
    textobject.textLines(texto)  # Insertamos el texto y con color gris
    c.drawText(textobject)  # Dibujamos el texto pasando un objeto de texto 
       
    c.showPage()
    c.save()
    
    return response

    