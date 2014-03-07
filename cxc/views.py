from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cxc.models import cuentaCobrar



@login_required(login_url='/')
def index(request):
    query = request.GET.get('q','')    
    if query:
        qset = (        
        Q(caberaId__clienteId__nombre__icontains=query)  )
          
        lista_cxc = cuentaCobrar.objects.filter(qset).distinct()
    else:
        lista_cxc = cuentaCobrar.objects.all()
    return render_to_response('adminCxc.html', {'cuentas':lista_cxc,}, context_instance=RequestContext(request))


@login_required(login_url='/')
def addAbono(request):
    return render_to_response('adminAbonoCxc.html', context_instance=RequestContext(request))
    