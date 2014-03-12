from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from caja.models import caja
import datetime



def index(request):       
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:    
        return HttpResponseRedirect('/login')


@login_required(login_url='/')   
def rCaja(request):
    if request.POST:
        cajaInicial = caja( created = datetime.datetime.now(),
                            createdby = str(request.user.id),
                            isactive = "Y",
                            updated = datetime.datetime.now(),
                            updatedby = str(request.user.id),
                            base = request.POST["txtbase"],
                            totalIngresos = 0,
                            totalEgresos = 0,
                            estado = 'O',
                            saldoCaja = request.POST["txtbase"],
                            fechaInicio = request.POST["txtfecha"],
                            fechaCierre = "1900-01-01"                                                   
                          )
        cajaInicial.save()
        return HttpResponseRedirect('/index')        
    return render_to_response('crearCaja.html', context_instance=RequestContext(request))
    
    