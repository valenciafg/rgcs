# coding: utf8
# intente algo como
@auth.requires_login()
def index():
    id_guardia = request.args(0) or redirect(URL('default','index'))
    import guardias
    import funciones
    import certificaciones
    import os
    import eventos
    editar=0
    turno=guardias.turno_guardia(id_guardia)
    festatus=None
    
    enlace_cambiar_estado=guardias.enlace_cambiar_estado(id_guardia)
    #Obtiene la imagen de estado del Enlaces si existe
    registro=db.guardias(id_guardia)
    if not registro.estatus_enlaces:
        img_enlaces="No hay archivo almacenado."
    else:
        img_enlaces=IMG(_src=URL('default','download',args=registro.estatus_enlaces))
        
    #Obtiene las observaciones de revision de guardia
    if not registro.observaciones_rev:
        observaciones_rev="No hay observaciones para esta guardia."
    else:
        observaciones_rev=registro.observaciones_rev
        observaciones_rev=HTML(XML(observaciones_rev.replace('\n','<br>')))
    observaciones=db.guardias(id_guardia).observaciones
    #Obtiene el reporte pdf generado al finalizar una guardia
    estado_inicial=guardias.estado_guardia(id_guardia)
    if estado_inicial!="En Proceso":
        reporte=A("Ver reporte",_href=URL('reportes','reporte_guardia',args=[id_guardia]),_target="blank")
    else:
        reporte=None
    enlace_eliminar=None
        
    #Se comprueba si la guardia está en estado 'Con Observaciones' o 'En Proceso', ésto para permitir editar
    if guardias.comprobar_estatus(id_guardia,funciones.id_usuario_actual()):
#        estado_inicial=guardias.estado_guardia(id_guardia)
        editar=1
        enlace_eliminar = SQLFORM.factory(Field('Eliminar','boolean'))
        btn = enlace_eliminar.element("input",_type="submit")
        btn["_onclick"] = "return confirm('Se eliminará la guardia junto con las certificaciones generadas. ¿Estás seguro que deseas eliminar esta guardia?');"
        if enlace_eliminar.process().accepted:
            eliminar_guardia(id_guardia)
        sw=None
        if estado_inicial=="En Proceso":
            #Se genera el formulario de cambiar estatus de guardia y almacenamiento de imagen de enlaces
            festatus=SQLFORM(db.guardias,registro,fields=['observaciones','estatus_enlaces'],
                         upload=URL('default','download'),
                         submit_button = 'Finalizar guardia')
            del festatus[0][0]
            if festatus.process().accepted:
                obs=festatus.vars.observaciones
                enlaces=festatus.vars.estatus_enlaces
                sw = db(db.guardias.id==id_guardia).update(observaciones=obs,
                                                      estatus="En Revisión",
                                                      estatus_enlaces=enlaces,
                                                      id_usuario_rev=None,
                                                      fecha_rev=None,
                                                      id_usuario_aprob=None,
                                                      fecha_aprob=None)
        else:
            #Se genera el formulario de cambiar estatus de guardia y almacenamiento de imagen de enlaces
            festatus=SQLFORM(db.guardias,registro,fields=['observaciones_rev_resp','estatus_enlaces'],
                         upload=URL('default','download'),
                         submit_button = 'Finalizar guardia')
            del festatus[0][0]
            if festatus.process().accepted:
                obs=festatus.vars.observaciones_rev_resp
                enlaces=festatus.vars.estatus_enlaces
                sw = db(db.guardias.id==id_guardia).update(observaciones_rev_resp=obs,
                                                      estatus="En Revisión",
                                                      estatus_enlaces=enlaces,
                                                      id_usuario_rev=None,
                                                      fecha_rev=None,
                                                      id_usuario_aprob=None,
                                                      fecha_aprob=None)
        if sw:
            if estado_inicial=="En Proceso":
                eventos.registar_evento(id_guardia,funciones.id_usuario_actual(),"Se ha finalizado una guardia")
            else:
                eventos.registar_evento(id_guardia,funciones.id_usuario_actual(),"Se ha actualizado una guardia")
            #Envia correo informativo al grupo rotativo desde la cuenta certificaciones@seguroscaroni.com
            import correo
            if correo.confirmar_guardia_correo(id_guardia):
                session.flash = T('Finalización de guardia registrado')
            else:
                session.flash = T('Problema al enviar correo de confirmación')
            redirect(URL('certificaciones','index',args=[id_guardia]))
    else:#Solo vista
        editar=0
    if not observaciones:
        observaciones="Sin Observaciones."
    else:
        observaciones=HTML(XML(observaciones.replace('\n','<br>')))
    logs=''
    if eventos.estado_logs()=='Activo':
        logs=eventos.listar_eventos(id_guardia)
    return dict(cat=consultar_actividades_turno(turno,id_guardia,editar),
                datos_guardia=guardias.datos_guardia(id_guardia),
                festatus=festatus,
                enlaces=img_enlaces,
                observaciones=observaciones,
                reporte=reporte,
                observaciones_rev=observaciones_rev,
                resp_observacion=guardias.resp_observaciones(id_guardia),
                enlace_cambiar_estado=enlace_cambiar_estado,
                enlace_eliminar=enlace_eliminar,
                logs=logs)

def eliminar_guardia(id_guardia):
    #redirect(URL('default','index'))
    if db(db.guardias.id == id_guardia).delete():
        session.flash = T('La guardia ha sido eliminada')
        redirect(URL('guardias','index'))
    else:
        session.flash = T('Ocurrio un error al eliminar la guardia')
        redirect(URL('guardias','mis_guardias'))
'''
    Listado de actividades correspondientes a un turno
'''
def consultar_actividades_turno(turno,guardia,editar):
    import tipos
    import certificaciones
    query=(db.checklist.id_actividades==db.actividades.id)&(db.actividades.estatus_act=='Activo')&(db.checklist.id_turnos==turno)
    filas=db(query).select(db.checklist.id,
                           db.checklist.id_actividades, 
                           db.actividades.desc_act, 
                           db.actividades.detalle_act,
                           db.checklist.horario,
                           orderby=db.checklist.horario|db.checklist.id)
    datos=[]
    datos.append(THEAD(TR(TH('#'),TH('Actividades'),TH('Tipo'),TH('Estatus'),TH('Horario'))))
    i=0
    enlace=None
    for registro in filas:
        estatus=certificaciones.estatus_certificacion(guardia,registro.checklist.id)
        festatus=None
        i=i+1
        if estatus:
            if estatus=="Generado":
                festatus=TD(estatus,_style='color:green;')
            else:
                festatus=TD(estatus,_style='color:orange;')
        else:
            festatus=TD("No Realizado",_style='color:red;')
        desc_tipo=tipos.tipo_actividad(registro.checklist.id_actividades)
        id_tipo=tipos.id_tipo_actividad(registro.checklist.id_actividades)
        if id_tipo>2:
            enlace= URL('certificaciones','farchivo',vars = dict(cl=registro.checklist.id,act=registro.checklist.id_actividades,g=guardia,edit=editar))
        else:
            enlace= URL('certificaciones','detalle',vars = dict(cl=registro.checklist.id,act=registro.checklist.id_actividades,g=guardia,edit=editar))
        detalle_act=registro.actividades.detalle_act
        if detalle_act==None:
            detalle_act="Sin información"
        datos.append(TR(TD(i),
                        TD(A(registro.actividades.desc_act,_href=enlace, **{'_title':detalle_act})),
                        desc_tipo,
                        festatus,
                        TD(registro.checklist.horario)))
    return TABLE(datos,_class="table table-hover")


'''
    Detalle de actividad de acuerdo al tipo de actividad (Sólo Logs y Checks). Incluye:
        -Vista
        -Formulario de inclusión
        -Formulario de Edición
'''
def detalle():
    id_act = request.vars.act or redirect(URL('default','index')) #ID ACTIVIDAD
    id_cl = request.vars.cl or redirect(URL('default','index'))   #ID CHECKLIST
    id_g = request.vars.g or redirect(URL('default','index'))     #ID GUARDIA
    editar = request.vars.edit or redirect(URL('default','index'))#SWITCH EDITAR 1 o 0
    import funciones
    import reportes
    #Retorna tipo y descripción de tipo de actividad
    import tipos
    id_tipo=tipos.id_tipo_actividad(id_act)
    desc_tipo=tipos.tipo_actividad(id_act)
    #Nombre de actividad
    import actividades
    nomb_actividad=actividades.nombre_actividad(id_act)
    titulo=H3(nomb_actividad)
    div_detalle=actividades.div_detalle_actividad(id_act)
    #Fecha de guardia
    import guardias
    fecha_g=guardias.fecha_guardia(id_g)
    #Retorno de fila de datos de certificación
    import certificaciones
    datos_certificacion=certificaciones.datos_certificacion(id_g,id_cl,id_act)
    import eventos
    evento=None
    if datos_certificacion:
        id_certificacion=datos_certificacion.certificaciones.id
        if id_certificacion and id_tipo>1:
            enlace="../../static/certificaciones/docs/"+str(fecha_g)+"-"+str(id_certificacion)+"-certificacion.pdf"
            link_reporte=LI(A("Ver reporte",_href=URL('reportes','reporte_certificacion',args=[id_g,id_certificacion]),_target="blank"))
        else:
            enlace="#"
            link_reporte=LI(A("Ver reporte",_href=URL("#")),_class="disabled")
        if id_certificacion:
            evento=eventos.listar_eventos_certificacion(id_certificacion)
    else:
        enlace="#"
        link_reporte=LI(A("Ver reporte",_href=URL("#")),_class="disabled")
    
    query=(db.certificaciones.id_guardia==id_g)&(db.certificaciones.id_checklist==id_cl)&(db.checklist.id==db.certificaciones.id_checklist)&(db.checklist.id_actividades==id_act)&(db.actividades.id==db.checklist.id_actividades)
    #Si editar es = a 1 entonces se modifica la fila (certificacion)
    if editar=="1":
        filas=db(query).select(db.certificaciones.id,
                               db.certificaciones.estatus,
                               db.certificaciones.detalle,
                               db.certificaciones.observaciones,
                               db.certificaciones.acciones_tomadas)
        #Actualizar una certificacion
        if filas:
            detalle=form_edit_detalle(id_tipo,filas)
            if detalle.process().accepted:
                if len(detalle.vars.observaciones)>0:
                    festatus="Con Observaciones"
                else:
                    festatus="Generado"
                id_cert=None
                for fila in filas:
                    id_cert=fila.id
                #si es 1 es check si es 2 es Logs
                if id_tipo==1:
                    db(db.certificaciones.id==id_cert).update(estatus=festatus,
                                                              observaciones=detalle.vars.observaciones,
                                                              acciones_tomadas=detalle.vars.acciones_tomadas)
                else:
                    db(db.certificaciones.id==id_cert).update(estatus=festatus, 
                                                              detalle=unicode(detalle.vars.detalle, 'utf8'),
                                                              observaciones=unicode(detalle.vars.observaciones, 'utf8'),
                                                              acciones_tomadas=unicode(detalle.vars.acciones_tomadas, 'utf8'))
                    session.flash="Actividad Modificada"
                eventos.registar_evento_certificacion(id_cert,funciones.id_usuario_actual(),"Se ha modificado la certificacion".encode("utf8"))
                redirect(URL('certificaciones','index',args=[id_g]))
        #FIN DE ACTUALIZACIÓN
        #Generar una nueva certificacion
        else:
            detalle=form_detalle(id_tipo)
            if id_tipo==1:
                if detalle.process().accepted:
                    if len(detalle.vars.observaciones)>0:
                        festatus="Con Observaciones"
                    else:
                        festatus="Generado"
                    id_cert=db.certificaciones.insert(id_guardia=id_g,
                                              id_checklist=id_cl,
                                              estatus=festatus,
                                              observaciones=unicode(detalle.vars.observaciones, 'utf8'),
                                              acciones_tomadas=unicode(detalle.vars.acciones_tomadas, 'utf8'))
                    eventos.registar_evento_certificacion(id_cert,funciones.id_usuario_actual(),"Se ha generado una certificacion".encode("utf8"))
                    session.flash = "Actividad registrada"
                    redirect(URL('certificaciones','index',args=[id_g]))
            elif id_tipo==2:
                if detalle.process().accepted:
                    if len(detalle.vars.observaciones)>0:
                        festatus="Con Observaciones"
                    else:
                        festatus="Generado"
                    id_cert=db.certificaciones.insert(id_guardia=id_g,
                                              id_checklist=id_cl,
                                              estatus=festatus,
                                              detalle=detalle.vars.detalle.encode('UTF-8','replace'),
                                              observaciones=detalle.vars.observaciones,
                                              acciones_tomadas=detalle.vars.acciones_tomadas)
                    eventos.registar_evento_certificacion(id_cert,funciones.id_usuario_actual(),"Se ha generado una certificacion".encode("utf8"))
                    session.flash = "Actividad registrada y reporte generado"
                    redirect(URL('certificaciones','index',args=[id_g]))
        #FIN DE GENERACIÓN
    #Ya existe la certificacion en la BD reportes.reporte_certificacion(38,28)
    else:
        detalle=mostrar_detalle(id_tipo,query)
    enlace=A('Regresar',_class="btn btn-primary btn-lg active", _role="button", _href=URL('certificaciones','index',args=[id_g]))
    return dict(detalle=detalle,
                div_detalle=div_detalle,
                titulo=titulo,
                link_reporte=link_reporte,
                enlace=enlace,
                evento=evento)
'''
    Generacion de un formulario de EDICION de acuerdo al tipo de Actividad
'''
def form_edit_detalle(tipo,filas):
    for fila in filas:
        id=fila.id
        detalle=fila.detalle
        observaciones=fila.observaciones
        acciones_tomadas=fila.acciones_tomadas
    #si es 1 es check si es 2 es documento
    if tipo==1:
        fedetalle=SQLFORM.factory(Field("observaciones","text",default=observaciones),
                                  Field("acciones_tomadas","text",default=acciones_tomadas),
                                  submit_button = 'Generar Certificación')
    else:
        fedetalle=SQLFORM.factory(Field("detalle","text", length=80000,default=detalle),#, widget=ckeditor.widget),
                                  Field("observaciones","text",default=observaciones),
                                  Field("acciones_tomadas","text",default=acciones_tomadas),
                                  submit_button = 'Generar Certificación')
    return fedetalle
'''
    Generacion de un formulario de INSERCION de acuerdo al tipo de Actividad
'''
def form_detalle(tipo):
    if (tipo==1):
        fdetalle=SQLFORM.factory(Field("observaciones", "text"),
                                 Field("acciones_tomadas", "text", default=None),
                                 submit_button = 'Generar Certificación')
    elif tipo==2:
        fdetalle=SQLFORM.factory(Field("detalle", "text", length=80000, default=None,label="Descripción del Servicio"),#, widget=ckeditor.widget),
                                 Field("observaciones", "text", default=None),
                                 Field("acciones_tomadas", "text", default=None),
                                 submit_button = 'Generar Certificación')
    return fdetalle
'''
    PROCESAR FORMULARIO DE ARCHIVOS/IMAGENES. INCLUYE:
    - VISTA DE FORMULARIO
    - ENLACE A VISTA (GENERACION) DE REPORTE PDF 
    - VISTA A ARCHIVOS A REEMPLAZAR
'''
def farchivo():
    id_act = request.vars.act or redirect(URL('default','index')) #ID ACTIVIDAD
    id_cl = request.vars.cl or redirect(URL('default','index'))   #ID CHECKLIST
    id_g = request.vars.g or redirect(URL('default','index'))     #ID GUARDIA
    editar = request.vars.edit or redirect(URL('default','index'))#SWITCH EDITAR 1 o 0
    import funciones
    import imagenes
    import reportes
    #Retorna tipo y descripción de tipo de actividad
    import tipos
    id_tipo=tipos.id_tipo_actividad(id_act)
    if id_tipo==3:
        extensiones = ['doc','docx','xls','xlsx','txt','log','pdf']
    else:
        extensiones = ['jpg','png']
    #Nombre de actividad
    import actividades
    nomb_actividad=actividades.nombre_actividad(id_act)
    titulo=H3(nomb_actividad)
     #Fecha de guardia
    import guardias
    fecha_g=guardias.fecha_guardia(id_g)
    #Retorno de fila de datos de certificación
    import eventos
    evento=None
    import certificaciones
    datos_certificacion=certificaciones.datos_certificacion(id_g,id_cl,id_act)
    if datos_certificacion:
        id_certificacion=datos_certificacion.certificaciones.id
        if id_certificacion and id_tipo==4:
            enlace="../../static/certificaciones/docs/"+str(fecha_g)+"-"+str(id_certificacion)+"-certificacion.pdf"
            link_reporte=LI(A("Ver reporte",_href=URL('reportes','reporte_certificacion_img',args=[id_g,id_certificacion]),_target="blank"))
        else:
            enlace="#"
            link_reporte=LI(A("Ver reporte",_href=URL("#")),_class="disabled")
        if id_certificacion:
            evento=eventos.listar_eventos_certificacion(id_certificacion)
    else:
        enlace="#"
        link_reporte=LI(A("Ver reporte",_href=URL("#")),_class="disabled")
        
    query=(db.certificaciones.id_guardia==id_g)&(db.certificaciones.id_checklist==id_cl)&(db.checklist.id==db.certificaciones.id_checklist)&(db.checklist.id_actividades==id_act)&(db.actividades.id==db.checklist.id_actividades)
    reemplazar=0
    archivos_reem=None
    if editar=="1":
        filas=db(query).select(db.certificaciones.id,
                       db.certificaciones.estatus,
                       db.certificaciones.detalle,
                       db.certificaciones.observaciones,
                       db.certificaciones.acciones_tomadas)
        #Actualizar una certificacion
        if filas:
            reemplazar=1
            archivos_reem=mostrar_detalle_archivos(id_tipo, query)
        fdetalle=SQLFORM.factory(db.archivos,
                             Field("observaciones", "text"),
                             Field("acciones_tomadas", "text", default=None))
        #if fdetalle.accepts(request, session):
        if fdetalle.accepts(request, session, onvalidation=lambda fdetalle:check(fdetalle,extensiones)):
            if len(fdetalle.vars.observaciones)>0:
                festatus="Con Observaciones"
            else:
                festatus="Generado"
            if reemplazar==1:
                for fila in filas:
                    db(db.archivos.id_certificacion == fila.id).delete()
                id_certi=db(db.certificaciones.id == fila.id).update(estatus=festatus,
                                                                     observaciones=fdetalle.vars.observaciones,
                                                                     acciones_tomadas=fdetalle.vars.acciones_tomadas)
                id_certi=fila.id
                eventos.registar_evento_certificacion(id_certi,funciones.id_usuario_actual(),"Se ha modificado la certificacion".encode("utf8"))
            else:
                id_certi=db.certificaciones.insert(id_guardia=id_g,
                                                   id_checklist=id_cl,
                                                   estatus=festatus,
                                                   observaciones=fdetalle.vars.observaciones,
                                                   acciones_tomadas=fdetalle.vars.acciones_tomadas)
                eventos.registar_evento_certificacion(id_certi,funciones.id_usuario_actual(),"Se ha generado una certificacion".encode("utf8"))
            nfiles = 0
            for var in request.vars:
                if var.startswith('archivo') and request.vars[var] != '':
                    
                    uploaded = request.vars[var]
                    if isinstance(uploaded,list):
                        # files uploaded through input with "multiple" attribute set on true
                        counter=0
                        for element in uploaded:
                            counter += 1
                            nfiles += 1
                            file_title = element.name.split(":")[-1]
                            ext=None
                            if not file_title:
                                ext=element.filename.split('.')[-1]
                                ext = "."+ext
                                file_title = element.filename
                                file_title = file_title.replace(ext,"")
                            id_archivo=db.archivos.insert(
                               id_certificacion=id_certi,
                                titulo=file_title,#+" ("+str(counter)+")" if file_title!="" else file_title,
                                archivo=db.archivos.archivo.store(element.file,element.filename))
                    else:
                        # only one file uploaded
                        element = request.vars[var]
                        nfiles += 1
                        file_title = element.name.split(":")[-1]
                        ext=None
                        if not file_title:
                            ext=element.filename.split('.')[-1]
                            ext = "."+ext
                            file_title = element.filename
                            file_title = file_title.replace(ext,"")
                        id_archivo=db.archivos.insert(
                           id_certificacion=id_certi,
                            titulo=file_title,
                            archivo=db.archivos.archivo.store(element.file,element.filename))
            session.flash = T('%s archivo%s cargado%s'%(nfiles, 's' if nfiles>1 else '','s' if nfiles>1 else ''))
            redirect(URL('certificaciones','index',args=[id_g]))
        del fdetalle[0][0] #Oculta el elemento titulo/descripción
        del fdetalle[0][0]
    else:
        fdetalle=mostrar_detalle_archivos(id_tipo, query)
    enlace=A('Regresar',_class="btn btn-primary btn-lg active", _role="button", _href=URL('certificaciones','index',args=[id_g]))
    return dict(titulo=titulo,
                form=fdetalle,
                enlace=enlace,
                reemplazar=reemplazar,
                archivos_reem=archivos_reem,
                link_reporte=link_reporte,
                evento=evento)

def vacio(variables):
    for var in variables:
        if var.startswith('archivo') and request.vars[var] != '':
            return True
    return False
    
def check(fdetalle,extensiones):
    variables=request.vars
    error = ""
    if vacio(variables):
        for var in variables:
            if var.startswith('archivo') and request.vars[var] != '':
                archivos = request.vars[var]
                if isinstance(archivos,list): #En caso de ser varios archivos
                    for archivo in archivos:
                        extension = archivo.filename.split('.')[-1]
                        if extension.lower() in extensiones:
                            pass
                        else:
                            error = error + "La extensión del archivo "+archivo.filename+" no es válida. "
                            #break
                else: #En caso de ser sólo un archivo
                    extension = archivos.filename.split('.')[-1]
                    if extension.lower() in extensiones:
                        pass
                    else:
                        error = error + "La extensión del archivo "+archivos.filename+" no es válida. "
        if error:
            fdetalle.errors.archivo = T(error)
        else:
            return
    else:
        fdetalle.errors.archivo = T("La lista de archivos está vacía")

def mostrar_detalle(tipo,query):
    filas=db(query).select(db.certificaciones.estatus,db.certificaciones.detalle,db.certificaciones.observaciones,db.certificaciones.acciones_tomadas)
    datos=[]
    for fila in filas:
        datos.append(TR(THEAD("Estatus: "),TD(fila.estatus)))
        if fila.detalle:
            fila.detalle=fila.detalle.replace("\n","<br>")
            datos.append(TR(THEAD("Detalle: "),TD(HTML(XML(fila.detalle)))))
        if fila.observaciones:
            datos.append(TR(THEAD("Observaciones: "),TD(fila.observaciones)))
        if fila.acciones_tomadas:
            datos.append(TR(THEAD("Acciones Tomadas: "),TD(fila.acciones_tomadas)))
    return TABLE(datos,_class="table table-hover")
def mostrar_detalle_archivos(tipo, query):
    filas=db(query).select(db.certificaciones.id,db.certificaciones.estatus,db.certificaciones.observaciones,db.certificaciones.acciones_tomadas)
    datos=[]
    id=None
    for fila in filas:
        datos.append(TR(THEAD("Estatus: "),TD(fila.estatus)))
        if fila.observaciones:
            datos.append(TR(THEAD("Observaciones: "),TD(fila.observaciones)))
        if fila.acciones_tomadas:
            datos.append(TR(THEAD("Acciones Tomadas: "),TD(fila.acciones_tomadas)))
        id=fila.id
    if id:
        query=(db.archivos.id_certificacion==id)
        filas=db(query).select(db.archivos.titulo,db.archivos.archivo)
        if tipo==3:
            titulo=None
            datos.append(TR(THEAD("Archivos ")))
            for fila in filas:
                titulo=fila.titulo
                if not titulo:
                    titulo="Archivo sin título"
                datos.append(TR(TD("Título: "+titulo),TD(A("Descargar Archivo",_href=URL("descargar",args=fila.archivo),_target='blank'))))
        else:
            titulo=None
            datos.append(TR(THEAD("Archivos ")))
            for fila in filas:
                titulo=fila.titulo
                if not titulo:
                    titulo=fila.archivo
                #datos.append(TR(TD("Título: "+titulo),TD(A("Descargar Archivo",_href=URL("descargar",args=fila.archivo),_target='blank'))))
                #IMG(_src=fila.archivo,_alt=titulo)
                datos.append(TR(TD("Título: "+titulo),TD(IMG(_src='/guardias/static/archivos/'+fila.archivo,_alt=titulo))))
    return TABLE(datos,_class="table table-hover")

def descargar():
    return response.download(request,db)
def vista():
	redirect(URL('static','archivos',args=request.args(0)))
    
def mostrar_eventos_certificacion(id):
    return False
