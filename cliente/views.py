from cliente.formularios import clienteForms
from cliente.models import cliente
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from reportlab.pdfgen import canvas
import datetime



@login_required(login_url='/')
def index(request):
    query = request.GET.get('q','')    
    if query:
        qset = (
        Q(nombre__icontains=query))
        lista_clientes = cliente.objects.filter(qset).distinct()
    else:
        lista_clientes =  cliente.objects.filter(isactive='Y').exclude(pk=1)
    return render_to_response('adminCliente.html', {'clientes':lista_clientes}, context_instance=RequestContext(request))


@login_required(login_url='/')
def registro(request):
    titulo = 'Registrar Tercero'
    if request.method == "POST":
        formulario = clienteForms(request.POST)
        if formulario.is_valid():
            ins_save = formulario.save( commit = False)
            ins_save.created =  datetime.datetime.now() 
            ins_save.createdby =  str(request.user.id)
            ins_save.isactive = 'Y'
            ins_save.updated = datetime.datetime.now() 
            ins_save.updatedby =  str(request.user.id)
            ins_save.save()
            return HttpResponseRedirect('/rclis')
    else:
        formulario = clienteForms()
    return render_to_response('crudCliente.html', {"formulario":formulario, "titulo":titulo,}, 
            context_instance= RequestContext(request))
    
@login_required(login_url='/')
def editarCliente(request, cliente_id):
    titulo = 'Editar Tercero'
    mensaje = ''
    cliente_edit = cliente.objects.get(pk=cliente_id)
    error = ''
    if request.method == 'POST':
        formulario = clienteForms( request.POST, instance=cliente_edit )
        if formulario.is_valid():
            ins_save = formulario.save( commit = False)
            ins_save.updated = datetime.datetime.now()
            ins_save.updatedby = str(request.user.id)            
            ins_save.save()
            return HttpResponseRedirect('/rclis')            
    else:
        formulario = clienteForms( instance=cliente_edit )
    return render_to_response('crudCliente.html', 
        {'formulario':formulario, "mensaje":mensaje, "titulo":titulo, "error":error}, 
        context_instance = RequestContext(request) )

@login_required(login_url='/')
def delCliente(request, cliente_id):
    if request.is_ajax and request.method == "GET":
        cliente_eliminar = cliente.objects.get(pk=cliente_id)
        cliente_eliminar.isactive = 'N'
        cliente_eliminar.updated = datetime.datetime.now()
        cliente_eliminar.updatedby = str(request.user.id)
        cliente_eliminar.save()        
        return HttpResponseRedirect('/')
    else:
        return Http404


@login_required(login_url='/')
def imprimir( request, texto ):
    query = texto    
    if query == '0':
        lista_clientes =  cliente.objects.filter(isactive='Y').exclude(pk=1)       
    else:
        qset = (
        Q(nombre__icontains=query))
        lista_clientes = cliente.objects.filter(qset).distinct()
    
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=cliente.pdf' 
    c = canvas.Canvas(response)    
      
    c = armazon(c, 'I') 
    x = 50
    y = 715
    contador = 0
    for i in lista_clientes:
        contador += 1
        c.drawRightString(90, y, i.identificacion) 
        c.drawString(130, y, i.nombre) 
        c.drawRightString(375, y, str(i.saldodeuda)) 
        c.drawRightString(465, y, str(i.saldofavor) )
        c.drawRightString(545, y, str(i.limitecredito ))        
        y = y - 12 
        if contador == 46:
            c.showPage()
            c = armazon(c, 'C')
            x = 50
            y = 775 
            contador = 0       
            
    c.showPage()
    c.save()
           
    return response



def armazon(c, pagina):
    y1 = 160 #cuadro grande
    y2 = 590 #cuadro grande
    y3 = 735 #titulos tabla 
    y4 = 750 #lineas verticales
    y5 = 730 #linea horizontal
    if pagina == 'I':
        #fuente para el titulo
        c.setFont("Helvetica", 24) 
        c.drawString(250, 800, 'Lista de Clientes Activos')
        c.drawString(100, 800, 'DAPLIW') 
        c.setFont("Helvetica", 16)
        c.drawString(100, 780, 'Nit: 890465322')
    else:
        y2 = 650
        y3 = 795 
        y4 = 810
        y5 = 790         
  
    c.roundRect(45,y1,515,y2,20,stroke=1, fill=0)
    c.setFont("Helvetica", 9)
    c.drawString(58, y3, 'Identificacion')
    c.drawString(190, y3, 'Nombre')
    c.drawString(330, y3, 'Saldo Deuda')
    c.drawString(415, y3, 'Saldo Favor')
    c.drawString(490, y3, 'Limite Credito')

    c.line(120,y4,120,y1)
    c.line(310,y4,310,y1)
    c.line(400,y4,400,y1)
    c.line(480,y4,480,y1)
    c.line(45,y5,560,y5) #horizontal

    c.roundRect(45,65,140,85,20,stroke=1, fill=0)
    c.roundRect(425,65,140,85,20,stroke=1, fill=0)

    c.setFont("Helvetica", 8)
    c.line(430,83,560,83)
    c.drawString(57, 70, 'FIRMA Y SELLO AUTORIZADO')
    c.drawString(433, 137, 'ACEPTADO') 
    c.drawString(450, 70, 'NOMBRE Y C.C O N.I.T') 

    return c
 