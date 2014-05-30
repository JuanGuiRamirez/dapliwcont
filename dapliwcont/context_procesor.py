

def crearMenu( request ):
    
    menus = { 'menu' : [
                { 'name' : 'Productos', 'url' : '/index/' },
                { 'name' : 'Terceros', 'url' : '/rclis/' },
                { 'name' : 'Factura Venta', 'url' : '/factV/' },
                { 'name' : 'Factura Compra', 'url' : '/factC/' },
                { 'name' : 'Caja', 'url' : '/clis/' },
                { 'name' : 'Creditos', 'url' : '/lcc/' },
                { 'name' : 'Cuentas por pagar', 'url' : '/lcxp/' },
                { 'name' : 'Reportes', 'url' : '/#' },
              
              ]}
    
    for item in menus['menu']:
        if request.path == item['url']:
            item['active'] = True        
    return menus   
   