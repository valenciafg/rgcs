# coding: utf8
@auth.requires_login()
#@auth.requires(auth& db.auth_user.user_type=='Administrador')
def index(): #tipos=SQLFORM.factory(db.tipos, labels = {'desc_tipo':'Descripción de tipo'})
    actividades=SQLFORM.factory(db.actividades,
                                submit_button = 'Generar actividad',
                                labels = {'desc_act':'Descripción de actividad',
                                          'id_tipos':'Tipo de actividad',
                                          'estatus_act':'Estado de actividad',
                                          'detalle_act':'Detalle de actividad'}
                                )
    if actividades.process().accepted:
        db.actividades.insert(desc_act=actividades.vars.desc_act,
                              id_tipos=actividades.vars.id_tipos,
                              estatus_act=actividades.vars.estatus_act)
        response.flash = 'Actividad Agregada'
    elif actividades.errors:
        error=actividades.errors.name
        response.flash = error
    return dict(actividades=actividades,actividades_actuales=consultar_actividades())

def editar_actividades():
    id = request.args[0] 
    registro=db.actividades(id) or redirect(URL('index'))
    form=SQLFORM(db.actividades,registro,deletable = True,labels = {'id':'Nro. de registro',
                                          'id_tipos':'Tipo de actividad',
                                          'estatus_act':'Estado de actividad',
                                          'desc_act':'Descripción de actividad',
                                          'detalle_act':'Detalle de actividad'})
    if form.process().accepted:
        session.flash = 'Se ha modificado una actividad'
        redirect(URL('actividades','index'))
    return dict(form=form)

def consultar_actividades():
    query=(db.actividades.id_tipos==db.tipos.id)
    filas=db(query).select(db.actividades.id, db.actividades.desc_act, db.actividades.estatus_act,db.tipos.desc_tipo)
    datos=[]
    datos.append(THEAD(TR(TH('#'),TH('Actividades'),TH('Estatus'),TH('Tipo'))))
    i=1
    enlace=None
    import funciones
    if funciones.tipo_usuario(funciones.id_usuario_actual())=='Administrador':
        sw=1
    else:
        sw=0
    for registro in filas:
        if registro.actividades.estatus_act=="Activo":
            estatus=TD(registro.actividades.estatus_act,_style='color:green;')
        else:
            estatus=TD(registro.actividades.estatus_act,_style='color:orange;')
        if sw==1:
            enlace=A(i,_href=URL('actividades','editar_actividades',args=[registro.actividades.id]))
        else:
            enlace=registro.actividades.id
        datos.append(TR(TD(enlace),
                        TD(registro.actividades.desc_act),
                        estatus,
                        TD(registro.tipos.desc_tipo)))
        i=i+1
    return TABLE(datos,_class="table table-hover")
