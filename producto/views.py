from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from producto.formularios import productoForms
from producto.models import producto
import datetime



@login_required(login_url='/')
def index(request):
    query = request.GET.get('q','')    
    if query:
        qset = (
        Q(nombre__icontains=query))
        lista_productos = producto.objects.filter(qset).distinct()
    else:
        lista_productos = producto.objects.all()        
    return render_to_response('adminProducto.html', {'productos':lista_productos,}, context_instance=RequestContext(request))
    

@login_required(login_url='/')
def registro(request):
    if request.method == "POST":
        formulario = productoForms(request.POST)
        if formulario.is_valid():
            ins_save = formulario.save( commit = False)
            ins_save.created =  datetime.datetime.now() 
            ins_save.createdby = str(request.user.id)
            ins_save.isactive = 'Y'
            ins_save.updated = datetime.datetime.now() 
            ins_save.updatedby = str(request.user.id),
            ins_save.save()
            return HttpResponseRedirect('/index')
    else:
        formulario = productoForms()
    return render_to_response('crudProducto.html', {"formulario":formulario}, 
            context_instance= RequestContext(request))
    

def editarProducto(request, producto_id):
    titulo = 'Editar Producto'
    mensaje = ''
    producto_edit = producto.objects.get(pk=producto_id)
    error = ''
    if request.method == 'POST':
        formulario = productoForms( request.POST, instance=producto_edit )
        if formulario.is_valid():
            ins_save = formulario.save( commit = False)
            ins_save.updated = datetime.datetime.now()
            ins_save.updatedby = str(request.user.id)
            if ins_save.preciocompra < ins_save.precioventa:
                ins_save.save()
                return HttpResponseRedirect('/index')
            else:
                error = 'El precio de compra debe ser menor que el precio de venta'
    else:
        formulario = productoForms( instance=producto_edit )
    return render_to_response('crudProducto.html', 
        {'formulario':formulario, "mensaje":mensaje, "titulo":titulo, "error":error}, 
        context_instance = RequestContext(request) )


def delProducto(request, producto_id): 
    if request.is_ajax and request.method == "GET":        
        producto_eliminar = producto.objects.get(pk=producto_id)
        producto_eliminar.delete()
        return HttpResponseRedirect('/index')
    else:
        return Http404
