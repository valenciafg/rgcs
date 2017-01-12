# coding: utf8
@auth.requires_login()
def index():
    form_checklist=SQLFORM.factory(db.checklist,
                            submit_button = 'Agregar al Checklist',
                            labels = {'id_actividades':'Actividad',
                                      'id_turnos':'Turno'}
                            )
    if form_checklist.process().accepted:
        db.checklist.insert(horario=form_checklist.vars.horario,
                            id_actividades=form_checklist.vars.id_actividades,
                            id_turnos=form_checklist.vars.id_turnos)
        response.flash = 'Actividad Agregada al Checklist'
    return dict(form_checklist=form_checklist, cl_manana=checklist_turnos(1), cl_tarde=checklist_turnos(2), cl_noche=checklist_turnos(3))

def editar_checklist():
    id = request.args[0]
    registro=db.checklist(id) or redirect(URL('index'))
    form=SQLFORM(db.checklist,registro,deletable = True,labels = {'id':'Nro. de registro',
                                                                  'horario':'Horario',
                 'id_actividades':'Actividades',
                 'id_turnos':'Turnos'})
    if form.process().accepted:
        session.flash = T('Se ha realizado una modificación a una actividad del checklist')
        redirect(URL('checklist','index'))
    return dict(form=form)

def checklist_turnos(turno):
    #query=(db.checklist.id_turnos==turno)&(db.checklist.id_actividades==db.actividades.id)&(db.actividades.estatus_act=='Activo')
    
    query=(db.checklist.id_turnos==turno)&(db.checklist.id_actividades==db.actividades.id)&(db.actividades.estatus_act=='Activo')

    #filas=db(query).select(db.checklist.id,
     #                      db.actividades.desc_act,
        #                     db.checklist.horario,
        #                   orderby=db.checklist.horario|db.checklist.id )
        
    filas=db(query).select(db.checklist.id,
                           db.actividades.desc_act,
                           db.checklist.horario,
                           #orderby=db.checklist.horario|db.checklist.id )
                           orderby=db.checklist.horario|db.checklist.id )
                               
    datos=[]
    datos.append(THEAD(TR(TH('#'),TH('Actividades'),TH('Horario'))))
    cont=1;
    import funciones
    if funciones.tipo_usuario(funciones.id_usuario_actual())=='Administrador':
    #if funciones.tipo_usuario(funciones.id_usuario_actual())=='Rotativo':
        sw=1
    else:
        sw=0
    for registro in filas:
        if sw==1:
            enlace=A(cont,_href=URL('checklist','editar_checklist',args=[registro.checklist.id]))
        else:
            enlace=registro.checklist.id
        datos.append(TR(TD(enlace),
                        TD(registro.actividades.desc_act),
                        TD(registro.checklist.horario)))
        cont=cont+1
    return TABLE(datos,_class="table table-hover")

def consultar_checklist():
    query=(db.checklist.id_turnos==db.turnos.id)&(db.checklist.id_actividades==db.actividades.id)&(db.actividades.estatus_act=='Activo')
    filas=db(query).select(db.checklist.id,
                           db.actividades.desc_act,
                           db.checklist.horario,
                           db.turnos.turno,
                           orderby=db.checklist.id_turnos|db.checklist.id|db.checklist.horario)
    datos=[]
    datos.append(THEAD(TR(TH('#'),TH('Actividades'),TH('Horario'),TH('Turno'))))
    cont=1
    import funciones
    if funciones.tipo_usuario(funciones.id_usuario_actual())=='Administrador':
    #if funciones.tipo_usuario(funciones.id_usuario_actual())=='Rotativo':
        sw=1
    else:
        sw=0
    for registro in filas:
        if sw==1:
            enlace=A(cont,_href=URL('checklist','editar_checklist',args=[registro.checklist.id]))
        else:
            enlace=registro.checklist.id
        datos.append(TR(TD(enlace),
                        TD(registro.actividades.desc_act),
                        TD(registro.checklist.horario),
                        TD(registro.turnos.turno)))
        cont=cont+1
    return TABLE(datos,_class="table table-hover")
