from caja.models import caja, ingreso, egreso
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime



@login_required(login_url='/')
def index(request):
    ing = ingreso.objects.all()[:5]
    egr = egreso.objects.all()[:5]
    cajas = caja.objects.filter(estado='C')
    cajaOpen = caja.cajaUso.all()
    contexto = {'ingLista' : ing, 'egrLista': egr,
                'totalIngresos' : cajaOpen[0].totalIngresos, 'totalEgresos' : cajaOpen[0].totalEgresos,
                'FechaInicio' : cajaOpen[0].fechaInicio,
                'cajas' : cajas, 'base': cajaOpen[0].base}
    return render_to_response('adminCaja.html', contexto , context_instance=RequestContext(request))

@login_required(login_url='/')
def rIngreso(request):
    cajaOpen = caja.cajaUso.all()    
    
    obj = ingreso(      created = datetime.datetime.now() ,
                        createdby = str(request.user.id),
                        isactive = "Y",
                        updated = datetime.datetime.now() ,
                        updatedby = str(request.user.id),                        
                        totalIngreso = request.POST['txtmontoIngreso'],    
                        fechaIngreso = request.POST['txtFechaIngreso'],
                        descripcion = request.POST['txtAreaIngreso'],
                        cajaId = cajaOpen[0].id  )                     
    obj.save()
    
@login_required(login_url='/')
def listarDetalle(request, mod):
    titulo = ''
    if mod == 'I':
        mvts = ingreso.objects.all()
        titulo = 'Lista de ingresos'
    else:
        mvts = egreso.objects.all()
        titulo = 'Lista de egresos'        
    return render_to_response('listDetalleCaja.html', { 'mvts' : mvts, 'mod' : mod, 
                                                       'titulo' : titulo },  context_instance=RequestContext(request))
    
    
   


    