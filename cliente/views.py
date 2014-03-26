from cliente.formularios import clienteForms
from cliente.models import cliente
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime



@login_required(login_url='/')
def index(request):
    query = request.GET.get('q','')    
    if query:
        qset = (
        Q(nombre__icontains=query))
        lista_clientes = cliente.objects.filter(qset).distinct()
    else:
        lista_clientes =  cliente.objects.all()        
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
            return HttpResponseRedirect('/')            
    else:
        formulario = clienteForms( instance=cliente_edit )
    return render_to_response('crudCliente.html', 
        {'formulario':formulario, "mensaje":mensaje, "titulo":titulo, "error":error}, 
        context_instance = RequestContext(request) )

@login_required(login_url='/')
def delCliente(request, cliente_id):
    if request.is_ajax and request.method == "GET":
        cliente_eliminar = cliente.objects.get(pk=cliente_id)
        cliente_eliminar.delete()
        return HttpResponseRedirect('/')
    else:
        return Http404

 