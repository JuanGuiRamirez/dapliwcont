from django.conf.urls import patterns, include, url
from proveedor.views import busquedaPro

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    url(r'^$', 'principal.views.index'),
    url(r'^rCaja/$', 'principal.views.rCaja'),
    
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),        
    url(r'^cerrar/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       
    url(r'^index/$', 'producto.views.index', name = 'index'),
    url(r'^rprod/$', 'producto.views.registro'),
    url(r'^eprod/(?P<producto_id>[^/]+)$', 'producto.views.editarProducto'),
    url(r'^dprod/(?P<producto_id>[^/]+)$', 'producto.views.delProducto'),
    
    url(r'^rclis/$', 'cliente.views.index'),
    url(r'^rcli/$', 'cliente.views.registro'),
    url(r'^ecli/(?P<cliente_id>[^/]+)$', 'cliente.views.editarCliente'),
    url(r'^dcli/(?P<cliente_id>[^/]+)$', 'cliente.views.delCliente'),
    
    url(r'^clis/$', 'caja.views.index'),
    url(r'^cing/$', 'caja.views.rIngreso'),
    
    url(r'^plis/$', 'proveedor.views.index'),
    url(r'^pA/$', 'proveedor.views.nitAjax'),
    
    url(r'^pAjax/$', busquedaPro.as_view()),
    
    url(r'^factV/$', 'factVenta.views.index'), 
    url(r'^factImp/$', 'factVenta.views.imprimirFact'), 
    
    url(r'^lcc/$', 'cxc.views.index'), 
    url(r'^abcc/(?P<cxcId>\d+)$', 'cxc.views.addAbono'),  
    url(r'^lfcc/(?P<cxcId>\d+)$', 'cxc.views.verCxc'),
    url(r'^detF/$', 'cxc.views.detalleFactura'),
    
    url(r'^detPDF/$', 'cxc.views.crearPDF'),    
 
    
    # Examples:
    # url(r'^$', 'dapliwcont.views.home', name='home'),
    # url(r'^dapliwcont/', include('dapliwcont.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
