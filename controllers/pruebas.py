# coding: utf8
# intente algo como
def index():
    import os
    #registro = db.archivos(request.args(0)) or redirect(URL('index'))
    url = URL('index','download')
    #formulario = SQLFORM.factory(Field('descripcion', requires=IS_NOT_EMPTY()),
    #                             Field('filename'),
    #                             Field('imagen', 'upload', uploadfolder=os.path.join(current.request.folder,'uploads/archivos'), uploadseparate=True))
    #formulario = SQLFORM(db.archivos, registro, deletable=True,
    #               upload=url, fields=['descripcion', 'imagen'])
    formulario = SQLFORM(db.archivos)
    filename="no"
    if formulario.vars.imagen!=None:
        formulario.vars.filename = formulario.vars.imagen.filename
        filename=formulario.vars.filename
    if formulario.process().accepted:
       # newid=db.archivos.insert(descripcion=formulario.vars.descripcion,
       #                          filename=filename,
       #                          imagen=formulario.vars.imagen)
        response.flash = 'formulario aceptado'
    elif formulario.errors:
        response.flash = 'el formulario tiene errores'
    return dict(formulario=formulario,filename=filename)
