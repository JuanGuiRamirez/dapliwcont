from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from producto.models import producto
import datetime



def index(request):
    productos = producto.objects.all()
    return render_to_response('compraProveedor.html', {"lista":productos}, context_instance=RequestContext(request))


def nitAjax(request):
    if request.is_ajax() and request.method == "POST":
        nit_pro = request.POST["nit"]
    else:
        return Http404

class busquedaPro(TemplateView):
    
    def get(self, request, *args, **kwargs):
        nit_pro = request.GET["nit"]
        print nit_pro