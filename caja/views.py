from caja.models import caja, ingreso
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime




def index(request):
    ing = ingreso.objects.all()
    return render_to_response('adminCaja.html', {'ingLista' : ing}, context_instance=RequestContext(request))


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
    
    
    
    
   
    
    
#def index(request):
#    if request.method == "POST":
#        data = str(request.POST.copy())        
#        dif = data.find("totalIngreso")
#        if dif:
#            form = ingresoForm(request.POST)
#        else:
#            form = egresoForm(request.POST)            
#        if form.is_valid():
#            ins_save = form.save( commit = False)
#            ins_save.created = datetime.datetime.now() 
#            ins_save.createdby = str(request.user.id)
#            ins_save.isactive = 'Y'
#            ins_save.updated = datetime.datetime.now() 
#            ins_save.updatedby = str(request.user.id)
#            ins_save.save()
#            return HttpResponseRedirect('/clis') 
#    else:         
#        formularioIngreso = ingresoForm()   
#        formularioEgreso = egresoForm()              
#    return render_to_response('adminCaja.html', 
#                              {'ingresoForm' : formularioIngreso, 'egresoForm' : formularioEgreso}, 
#                              context_instance=RequestContext(request))


   


    