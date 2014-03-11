from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext



def index(request):
    usuario = request.user    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:    
        return HttpResponseRedirect('/login')


@login_required(login_url='/')   
def rCaja(request):
    return render_to_response('crearCaja.html', context_instance=RequestContext(request))
    
    