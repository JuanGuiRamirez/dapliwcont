from cxc.formularios import abonoForm
from cxc.models import cuentaCobrar, abono, cabeceraCxc
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from factVenta.models import productoVenta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime



@login_required(login_url='/')
def index(request):
    query = request.GET.get('q','')    
    if query:
        qset = (        
        Q(clienteId__nombre__icontains=query)  )
          
        lista_cxc = cabeceraCxc.objects.filter(qset).distinct()
    else:
        lista_cxc = cabeceraCxc.objects.all()
    return render_to_response('adminCxc.html', {'cuentas':lista_cxc,}, context_instance=RequestContext(request))


@login_required(login_url='/')
def addAbono(request, cxcId):
    cuenta = cabeceraCxc.objects.get(pk=cxcId)
    errores = ''
    if request.method == 'POST':
        formulario = abonoForm( request.POST )        
        if formulario.is_valid():
            ins_save = formulario.save( commit = False)
            if ins_save.montoAbono > 0:
                ins_save.created =  datetime.datetime.now() 
                ins_save.createdby =  str(request.user.id)
                ins_save.isactive = 'Y'
                ins_save.updated = datetime.datetime.now()                
                ins_save.updatedby =  str(request.user.id)  
                ins_save.saldoInicial = cuenta.totalDeudaGeneral
                ins_save.saldoFinal = cuenta.totalDeudaGeneral - ins_save.montoAbono
                ins_save.cuentaId_id = cxcId             
                cuenta.totalAbonosGeneral = cuenta.totalAbonosGeneral + ins_save.montoAbono
                cuenta.totalDeudaGeneral = cuenta.totalDeudaGeneral - ins_save.montoAbono
                ins_save.save()
                cuenta.save()
                formulario = abonoForm() 
            else:
                errores = 'Ingrese un monto valido'       
    else:
        formulario = abonoForm()    
    abonos = abono.objects.filter(cuentaId_id = cxcId).order_by('-created')
    return render_to_response('adminAbonoCxc.html', 
                              {'cuenta':cuenta, 'ab':abonos, 'formulario':formulario, 'error': errores}, 
                              context_instance=RequestContext(request))



@login_required(login_url='/')
def verCxc(request, cxcId):
    cuenta = cuentaCobrar.objects.filter(cabeceraId_id=cxcId)    
    return render_to_response('listCxc.html', {'cuentas':cuenta, 'idRegreso': cuenta[0].cabeceraId_id}, context_instance=RequestContext(request))


@login_required(login_url='/')
def detalleFactura(request, facturaId):
    prod =  productoVenta.objects.filter(cabecera_id = facturaId)
    fact = cuentaCobrar.objects.filter(facturaId_id = facturaId) 
    forma = ''
    if fact[0].facturaId.formaPago == 'F':
        forma = 'Credito'
    else:
        forma = 'Contado'  
    
    return render_to_response('detalleFactura.html', {'productos':prod, 'cliente': fact[0].facturaId.clienteId,
                                                      'fecha': fact[0].facturaId.fechaFactura,
                                                      'numFact': fact[0].facturaId.numeroFactura,
                                                      'valNeto': fact[0].facturaId.totalNeto,
                                                      'valDesc': fact[0].facturaId.totalDescuento,
                                                      'valTotal': fact[0].facturaId.totalPagar,
                                                      'cabecera':facturaId,
                                                      'forma_pago' : forma},
                                                    context_instance=RequestContext(request))


def crearPDF(request):
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
