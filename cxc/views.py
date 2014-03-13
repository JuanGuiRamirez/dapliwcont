from cxc.formularios import abonoForm
from cxc.models import cuentaCobrar, abono, cabeceraCxc
from factVenta.models import productoVenta
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
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
    if request.method == 'POST':
        formulario = abonoForm( request.POST )
        if formulario.is_valid():
            ins_save = formulario.save( commit = False)
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
    abonos = abono.objects.filter(cuentaId_id = cxcId)
    return render_to_response('adminAbonoCxc.html', {'cuenta':cuenta, 'ab':abonos, 'formulario':formulario}, context_instance=RequestContext(request))



@login_required(login_url='/')
def verCxc(request, cxcId):
    cuenta = cuentaCobrar.objects.filter(cabeceraId_id=cxcId)    
    return render_to_response('listCxc.html', {'cuentas':cuenta, 'idRegreso': cuenta[0].cabeceraId_id}, context_instance=RequestContext(request))


@login_required(login_url='/')
def detalleFactura(request):
    prod =  productoVenta.objects.filter(cabecera_id = 3)
    fact = cuentaCobrar.objects.filter(facturaId_id = 3) 
    return render_to_response('detalleFactura.html', {'productos':prod, 'cliente': fact[0].facturaId.clienteId,
                                                      'fecha': fact[0].facturaId.fechaFactura,
                                                      'numFact': fact[0].facturaId.numeroFactura,
                                                      'valNeto': fact[0].facturaId.totalNeto,
                                                      'valDesc': fact[0].facturaId.totalDescuento,
                                                      'valTotal': fact[0].facturaId.totalPagar},
                               context_instance=RequestContext(request))

