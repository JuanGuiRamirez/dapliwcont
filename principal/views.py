from caja.models import caja
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
import time



def index(request):       
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:    
        return HttpResponseRedirect('/login')


@login_required(login_url='/')   
def rCaja(request):
    errores = []
    if request.POST:
        base = request.POST["txtbase"]
        fecha = request.POST["txtfecha"]
        if base:
            if fecha:     
                cajaInicial = caja( created = datetime.datetime.now(),
                                createdby = str(request.user.id),
                                isactive = "Y",
                                updated = datetime.datetime.now(),
                                updatedby = str(request.user.id),
                                base = request.POST["txtbase"],
                                totalIngresos = 0,
                                totalEgresos = 0,
                                estado = 'O',
                                saldoCaja = base,
                                fechaInicio = request.POST["txtfecha"],
                                fechaCierre = "1900-01-01"                                                   
                              )
                cajaInicial.save()
                return HttpResponseRedirect('/index')
            else:
                errores.append('ingrese una fecha')                   
        else:
            errores.append('Ingrese un valor para la base')
            if not fecha:
                errores.append('ingrese una fecha de inicio para la caja') 
                                                          
    return render_to_response('crearCaja.html', {'errores':errores}, context_instance=RequestContext(request))
    
    