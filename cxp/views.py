from cxp.models import cabeceraCxp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext



@login_required(login_url='/')
def index(request):
    lista_cxp = cabeceraCxp.objects.all()
    return render_to_response('adminCxp.html', {'cxp':lista_cxp,}, context_instance=RequestContext(request))