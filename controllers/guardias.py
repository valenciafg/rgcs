# coding: utf8
# intente algo como
@auth.requires_login()
def index():
    newid=0
    import funciones, datetime, eventos
    id_usuario_act = funciones.id_usuario_actual()
    nombre_usuario_act= funciones.nombre_usuario_actual()
    fields=['fecha','turno','id_usuario']
    #Formulario de Creación de Guardias
    guardias=SQLFORM.factory(Field("fecha", "date", notnull=True,label="Fecha",requires=IS_DATE_IN_RANGE(maximum=datetime.date.today(),error_message='La fecha que ingresó no es válida')),
                             Field("turno", db.turnos,requires=IS_IN_DB( db, 'turnos.id', ' %(turno)s'), label="Turnos"),
                             Field("id_usuario",  default=nombre_usuario_act, writable=False, label="Usuario"))
    #Formulario de Consulta de Guardias por Fecha
    cguardias=SQLFORM.factory(Field("cfecha", "date", notnull=True,label="Fecha de guardia"),
                              submit_button="Consultar")

    if guardias.process(formname='form1',onvalidation=validar).accepted:
        newid=db.guardias.insert(id_usuario=id_usuario_act,
                                 fecha=guardias.vars.fecha,
                                 turno=guardias.vars.turno)
        session.flash = T('Nueva guardia creada')
        eventos.registar_evento(newid,id_usuario_act,"Se ha generado una guardia")
        redirect(URL('certificaciones','index',args=[newid]))

    if cguardias.process(formname='form2').accepted:
        redirect(URL('guardias','por_fecha',vars = dict(fecha=cguardias.vars.cfecha)))
    return dict(id_usuario_act=id_usuario_act,guardias=guardias,cguardias=cguardias)

def por_fecha():
    import guardias
    import time
    fecha = request.vars.fecha or redirect(URL('guardias','index'))
    tfguardias=None
    tfguardias=guardias.guardias_fecha(fecha)
    fecha=time.strptime(fecha,"%Y-%m-%d")
    fecha2="%d/%d/%d" % (fecha[2],fecha[1],fecha[0])
    return dict(guardias=tfguardias,fecha=fecha2)

def validar(form):
    guardia_miusuario=fecha_turno_miusuario_guardia(form)
    guardia_otrousuario=fecha_turno_otrousuario_guardia(form)
    if guardia_miusuario:
        redirect(URL('certificaciones','index',args=[guardia_miusuario]))
    elif guardia_otrousuario:
        session.flash='Otro usuario ya tiene registrada una guardia para la fecha y turno ingresado'
        redirect(URL('certificaciones','index',args=[guardia_otrousuario]))
    elif validar_rotativo():
        session.flash='Su tipo de usuario no puede crear guardias'
        redirect(URL('guardias','index'))
        
#Retorna el id de la guardia del usuario actualmente conectado en caso de que se encuentre en la BD
def fecha_turno_miusuario_guardia(form):
    import funciones
    id_usuario_act = funciones.id_usuario_actual()
    query=(db.guardias.fecha==form.vars.fecha)&(db.guardias.turno==form.vars.turno)&(db.guardias.id_usuario==id_usuario_act)
    result=db(query).select(db.guardias.id)
    id=None
    for fila in result:
        id=fila.id
    return id

def fecha_turno_otrousuario_guardia(form):
    import funciones
    id_usuario_act = funciones.id_usuario_actual()
    query=(db.guardias.fecha==form.vars.fecha)&(db.guardias.turno==form.vars.turno)&(db.guardias.id_usuario!=id_usuario_act)
    result=db(query).select(db.guardias.id)
    id=None
    for fila in result:
        id=fila.id
    return id

def validar_rotativo():
    import funciones
    id_usuario_act = funciones.id_usuario_actual()
    if funciones.tipo_usuario(id_usuario_act)=='Rotativo':
        return None
    else:
        return True
@auth.requires_login()
def mis_guardias():
    import funciones
    import guardias
    id_usuario_act = funciones.id_usuario_actual()
    tipo=funciones.tipo_usuario(id_usuario_act)
    titulo=H3("Guardias con Observaciones")
    if tipo=='Rotativo':
        datos=guardias.bandeja_rotativo(id_usuario_act)
        titulo=H3("Guardias Culminadas")
        datos2=guardias.bandeja_culminadas_rotativo(id_usuario_act)
    elif tipo=='Supervisor':
        datos=guardias.bandeja_supervisor(id_usuario_act)
        datos2=guardias.guardias_con_observaciones(id_usuario_act,1)
    else:
        datos=guardias.bandeja_administrador(id_usuario_act)
        datos2=guardias.guardias_con_observaciones(id_usuario_act,2)
    return dict(datos=datos,tipo=tipo,titulo=titulo,datos2=datos2)

#Guardias retornadas por proceso de revision o aprobacion
def guardias_obs(id_usuario_act,tipo):
    if tipo=='Supervisor':
        query=(db.guardias.estatus=='Con Observaciones')&(db.guardias.id_usuario_rev==id_usuario_act)
    elif tipo=="Administrador":
        query=(db.guardias.estatus=='Con Observaciones')&(db.guardias.id_usuario_aprob==id_usuario_act)

def cambiar_estado():
    id_g = request.vars.g or redirect(URL('default','index'))
    import funciones
    import guardias
    import time
    
    id_usuario_act = funciones.id_usuario_actual()
    tipo=funciones.tipo_usuario(id_usuario_act)
    if tipo=="Administrador":
        testados=['Aprobado','Con Observaciones']
    else:
        testados=['Por Aprobar','Con Observaciones']
    fcestado=SQLFORM.factory(Field("estatus", requires=IS_IN_SET(testados), default='Con Observaciones'),
                                 Field("observaciones", "text"),
                                 submit_button='Cambiar Estado')
    if fcestado.process().accepted:
        obs=fcestado.vars.observaciones
        fecha_actual=time.strftime("%Y-%m-%d")
        if tipo=="Administrador":
            db(db.guardias.id==id_g).update(observaciones_rev=obs,
                                            estatus=fcestado.vars.estatus,
                                            id_usuario_aprob=id_usuario_act,
                                            fecha_aprob=fecha_actual)
        else:
            db(db.guardias.id==id_g).update(observaciones_rev=obs,
                                            estatus=fcestado.vars.estatus,
                                            id_usuario_rev=id_usuario_act,
                                            fecha_rev=fecha_actual)
        import eventos
        evento="Se ha modificado el estatus a "+fcestado.vars.estatus
        eventos.registar_evento(id_g,id_usuario_act,evento)
        import correo
        if correo.cambio_estado_guardia_correo(id_g,funciones.nombre_completo(id_usuario_act),obs):
            session.flash = T('Cambio de estado de guardia registrado')
        else:
            session.flash = T('Problema al enviar correo de confirmación')
        import reportes
        if not(reportes.reporte_guardia(id_g)):
            session.flash = T('Se presentaron errores en la generación del reporte digital de la guardia')
        #import certificaciones
        #if not(certificaciones.actualizar_reportes_certificaciones(id_g,fcestado.vars.estatus)):
        #    session.flash = T('Se presentaron errores en la actualización de los reportes de certificaciones')
        redirect(URL('guardias','mis_guardias'))
    regresar=A('Regresar',_class="btn btn-primary btn-lg active", _role="button", _href=URL('guardias','mis_guardias'))
    return dict(datos_guardia=guardias.datos_guardia(id_g),
                fcestado=fcestado,
                regresar=regresar)

@auth.requires_login()
def admon_guardias():
    import eventos, funciones
    id_usuario_act = funciones.id_usuario_actual()
    tipo=funciones.tipo_usuario(id_usuario_act)
    if tipo=="Administrador":
        estado=eventos.estado_logs()
        opcion_disponible=None
        if estado=='Activo':
            estado=P(B(estado,_style='color:green;'))
            opcion_disponible='Inactivo'
        else:
            estado=P(B(estado,_style='color:red;'))
            opcion_disponible='Activo'

        fcestado=SQLFORM.factory(Field("estatus", requires=IS_IN_SET([opcion_disponible]), default=opcion_disponible),
                                 submit_button='Cambiar Estado')
        if fcestado.process(formname='form1').accepted:
            db(db.estado_historial_eventos.id == 1).update(estatus=fcestado.vars.estatus)
            session.flash = T('Fue cambiado el estado del historial de eventos')
            redirect(URL('guardias','admon_guardias'))
        feliminar=SQLFORM.factory(Field("id_guardia", requires=IS_INT_IN_RANGE(0,1e100),label="Número de guardia"),
                                 submit_button='Eliminar Guardia')
        if feliminar.process(formname='form2').accepted:
            import guardias
            if guardias.guardia_existe(feliminar.vars.id_guardia)>0:
                db(db.guardias.id == feliminar.vars.id_guardia).delete()
                session.flash = T('La guardia fue eliminada')
            else:
                session.flash = T('La guardia no puede ser eliminada debido a que no existe registrada')
            redirect(URL('guardias','admon_guardias'))
    else:
        session.flash = T('Debe ser un usuario administrador para ingresar a este módulo')
        redirect(URL('guardias','mis_guardias'))
    #if fcestado.process(formname='form2').accepted:
    #redirect(URL('guardias','admon_guardias'))
    return dict(estado=DIV(estado),
                fcestado=fcestado,
                feliminar=feliminar)#,check_log=check_log),_style='color:orange;'
