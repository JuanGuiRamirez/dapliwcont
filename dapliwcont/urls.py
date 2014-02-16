from django.conf.urls import patterns, include, url
from proveedor.views import busquedaPro

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
                       
    url(r'^$', 'producto.views.index'),
    url(r'^rprod/$', 'producto.views.registro'),
    url(r'^eprod/(?P<producto_id>[^/]+)$', 'producto.views.editarProducto'),
    url(r'^dprod/(?P<producto_id>[^/]+)$', 'producto.views.delProducto'),
    
    url(r'^rclis/$', 'cliente.views.index'),
    url(r'^rcli/$', 'cliente.views.registro'),
    url(r'^ecli/(?P<cliente_id>[^/]+)$', 'cliente.views.editarCliente'),
    url(r'^dcli/(?P<cliente_id>[^/]+)$', 'cliente.views.delCliente'),
    
    url(r'^plis/$', 'proveedor.views.index'),
    url(r'^pA/$', 'proveedor.views.nitAjax'),
    
    url(r'^pAjax/$', busquedaPro.as_view()),
    
    url(r'^factV/$', 'factVenta.views.index'),    
    
    # Examples:
    # url(r'^$', 'dapliwcont.views.home', name='home'),
    # url(r'^dapliwcont/', include('dapliwcont.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
