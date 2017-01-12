#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

def registar_evento(id_guardia, id_usuario, evento):
    import datetime
    fecha_hora=datetime.datetime.today()
    current.db.historial_eventos.insert(id_guardia=id_guardia,
                                        evento=evento,
                                        id_usuario=id_usuario,
                                        fecha_hora=fecha_hora)
    
def listar_eventos(id_guardia):
    import datetime
    datos=[]
    datos.append(THEAD(TR(TH('#'),TH('Evento'),TH('Fecha/Hora'),TH('Realizado por'))))
    query=(current.db.historial_eventos.id_guardia==id_guardia)&(current.db.auth_user.id==current.db.historial_eventos.id_usuario)
    filas=current.db(query).select(current.db.historial_eventos.evento,
                                  current.db.historial_eventos.fecha_hora,
                                  current.db.auth_user.first_name,
                                  orderby=current.db.historial_eventos.fecha_hora)
    cont=0
    for registros in filas:
        cont=cont+1
        datos.append(TR(TD(cont),
                        TD(registros.historial_eventos.evento),
                        TD(registros.historial_eventos.fecha_hora.strftime("%d/%m/%Y %H:%M:%S")),
                        TD(registros.auth_user.first_name)))
    return TABLE(datos,_class="table table-hover")

def estado_logs():
    estado=None
    query=(current.db.estado_historial_eventos.id==1)
    filas=current.db(query).select(current.db.estado_historial_eventos.estatus)
    for fila in filas:
        estado=fila.estatus
    return estado
def registar_evento_certificacion(id_certificacion, id_usuario, evento):
    import datetime
    fecha_hora=datetime.datetime.today()#.decode("utf8").encode("latin1")
    current.db.historial_eventos_certificacion.insert(id_certificacion=id_certificacion,
                                        evento=evento,
                                        id_usuario=id_usuario,
                                        fecha_hora=fecha_hora)

def listar_eventos_certificacion(id_certificacion):
    import datetime
    datos=[]
    datos.append(THEAD(TR(TH('#'),TH('Evento'),TH('Fecha/Hora'),TH('Realizado por'))))
    query=(current.db.historial_eventos_certificacion.id_certificacion==id_certificacion)&(current.db.auth_user.id==current.db.historial_eventos_certificacion.id_usuario)
    filas=current.db(query).select(current.db.historial_eventos_certificacion.evento,
                                  current.db.historial_eventos_certificacion.fecha_hora,
                                  current.db.auth_user.first_name,
                                  orderby=current.db.historial_eventos_certificacion.fecha_hora)
    cont=0
    for registros in filas:
        cont=cont+1
        datos.append(TR(TD(cont),
                        TD(registros.historial_eventos_certificacion.evento),
                        TD(registros.historial_eventos_certificacion.fecha_hora.strftime("%d/%m/%Y %H:%M:%S")),
                        TD(registros.auth_user.first_name)))
    return TABLE(datos,_class="table table-hover")
