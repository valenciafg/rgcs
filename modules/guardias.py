#!/usr/bin/env python
# coding: utf8
from gluon import *

def guardia_existe(id):
    query=(current.db.guardias.id==id)
    filas=current.db(query).select(current.db.guardias.id)
    nro=0
    for fila in filas:
        nro=fila.id
    return nro
def turno_guardia(id):
    query=(current.db.guardias.id==id)
    filas=current.db(query).select(current.db.guardias.turno)
    for fila in filas:
        turno=fila.turno
    return turno
def resp_observaciones(id):
    query=(current.db.guardias.id==id)
    filas=current.db(query).select(current.db.guardias.observaciones_rev_resp)
    resp=None
    for fila in filas:
        resp=fila.observaciones_rev_resp
    return resp
def fecha_guardia(id):
    query=(current.db.guardias.id==id)
    filas=current.db(query).select(current.db.guardias.fecha)
    for fila in filas:
        fecha=fila.fecha
    return fecha
def estado_guardia(id):
    query=(current.db.guardias.id==id)
    filas=current.db(query).select(current.db.guardias.estatus)
    for fila in filas:
        estatus=fila.estatus
    return estatus

def bandeja_supervisor(id_user):
    #|(current.db.guardias.estatus=='Por Aprobar')
    query=((current.db.guardias.estatus=='En Revisión'))&(current.db.turnos.id==current.db.guardias.turno)
    tabla=presentar_datos(query,1)
    return tabla
def bandeja_administrador(id_user):
    query=(current.db.guardias.estatus=='Por Aprobar')&(current.db.turnos.id==current.db.guardias.turno)
    tabla=presentar_datos(query,2)
    return tabla

def bandeja_rotativo(id_user):
    query=(current.db.guardias.id_usuario==id_user)&(current.db.guardias.estatus!="Aprobado")&(current.db.turnos.id==current.db.guardias.turno)
    #query=(current.db.guardias.id_usuario==id_user)&((current.db.guardias.estatus=="En Proceso")|(current.db.guardias.estatus=="En Revisión"))&(current.db.turnos.id==current.db.guardias.turno)
    filas=current.db(query).select(current.db.guardias.id,
                                   current.db.guardias.id_usuario,
                                   current.db.guardias.fecha,
                                   current.db.turnos.turno,
                                   current.db.guardias.estatus,
                                   current.db.guardias.observaciones_rev,
                                   current.db.guardias.id_usuario_rev,
                                   orderby=~current.db.guardias.fecha)
    tabla=presentar_datos_rotativo(filas)
    return tabla
def bandeja_culminadas_rotativo(id_user):
    query=(current.db.guardias.id_usuario==id_user)&(current.db.guardias.estatus=="Aprobado")&(current.db.turnos.id==current.db.guardias.turno)
    filas=current.db(query).select(current.db.guardias.id,
                                   current.db.guardias.id_usuario,
                                   current.db.guardias.fecha,
                                   current.db.turnos.turno,
                                   current.db.guardias.estatus,
                                   current.db.guardias.observaciones_rev,
                                   current.db.guardias.id_usuario_rev,
                                   orderby=~current.db.guardias.id,limitby=(0,8))
    tabla=presentar_datos_rotativo(filas)
    return tabla
def datos_guardia_correo(id):
    import funciones
    query=(current.db.guardias.id==id)&(current.db.turnos.id==current.db.guardias.turno)
    filas=current.db(query).select(current.db.guardias.id_usuario,current.db.guardias.fecha,current.db.turnos.turno,current.db.guardias.estatus)
    usuario=None
    fecha=None
    turno=None
    estatus= None
    correo= None
    for registro in filas:
        usuario=funciones.nombre_completo(registro.guardias.id_usuario)
        fecha=registro.guardias.fecha.strftime("%d/%m/%Y")
        turno=registro.turnos.turno
        estatus=registro.guardias.estatus
        correo=funciones.correo_usuario(registro.guardias.id_usuario)
    return usuario,fecha,turno,estatus,correo

def datos_guardia(id):
    import funciones
    #usuario = funciones.nombre_usuario(id)
    query=(current.db.guardias.id==id)&(current.db.guardias.turno==current.db.turnos.id)
    tabla=presentar_datos(query,0)
    return tabla

def guardias_fecha(fecha):
    import funciones
    query=(current.db.guardias.fecha==fecha)&(current.db.guardias.turno==current.db.turnos.id)
    tabla=presentar_datos(query,0)
    return tabla
#
    #BANDEJA DE GUARDIAS CON OBSERVACION
#
def guardias_con_observaciones(id,tipo_usuario):
    import os
    import funciones
    datos=[]
    datos.append(THEAD(TR(TH('Fecha de Gerneración'),TH('Fecha de Observación'),TH('Usuario'),TH('Turno'),TH('Estatus'),TH('Observación'),TH('Reporte'))))
    if tipo_usuario==1:
        query=(current.db.guardias.id_usuario_rev==id)&(current.db.guardias.estatus=="Con Observaciones")&(current.db.turnos.id==current.db.guardias.turno)
        filas=current.db(query).select(current.db.guardias.id,
                                       current.db.guardias.fecha,
                                       current.db.guardias.fecha_rev,
                                       current.db.guardias.id_usuario,
                                       current.db.turnos.turno,
                                       current.db.guardias.estatus,
                                       current.db.guardias.observaciones_rev)
        for registro in filas:
            datos.append(TR(TD(registro.guardias.fecha.strftime("%d/%m/%Y")),
                            TD(registro.guardias.fecha_rev.strftime("%d/%m/%Y")),
                            TD(funciones.nombre_completo(registro.guardias.id_usuario)),
                            TD(A(registro.turnos.turno,_href=URL('certificaciones','index',args=[registro.guardias.id]))),
                            TD(registro.guardias.estatus,_style='color:orange;'),
                            TD(registro.guardias.observaciones_rev),
                            TD(A("Ver",_href=URL('reportes','reporte_guardia',args=[registro.guardias.id]), _target='new'))))
    else:
        query=(current.db.guardias.id_usuario_aprob==id)&(current.db.guardias.estatus=="Con Observaciones")&(current.db.turnos.id==current.db.guardias.turno)
        filas=current.db(query).select(current.db.guardias.id,
                                       current.db.guardias.fecha,
                                       current.db.guardias.fecha_aprob,
                                       current.db.guardias.id_usuario,
                                       current.db.turnos.turno,
                                       current.db.guardias.estatus,
                                       current.db.guardias.observaciones_rev)
        for registro in filas:
            datos.append(TR(TD(registro.guardias.fecha.strftime("%d/%m/%Y")),
                            TD(registro.guardias.fecha_aprob.strftime("%d/%m/%Y")),
                            TD(funciones.nombre_completo(registro.guardias.id_usuario)),
                            TD(A(registro.turnos.turno,_href=URL('certificaciones','index',args=[registro.guardias.id]))),
                            TD(registro.guardias.estatus,_style='color:orange;'),
                            TD(registro.guardias.observaciones_rev),
                            TD(A("Ver",_href=URL('reportes','reporte_guardia',args=[registro.guardias.id]), _target='new'))))
    return TABLE(datos,_class="table table-hover")

def presentar_datos(query,editar):
    import funciones
    import os
    filas=current.db(query).select(current.db.guardias.id,
                                   current.db.guardias.id_usuario,
                                   current.db.guardias.fecha,
                                   current.db.turnos.turno,
                                   current.db.guardias.estatus,
                                   orderby=~current.db.guardias.fecha)
    datos=[]
    estatus= None
    datos.append(THEAD(TR(TH('Usuario'),TH('Fecha'),TH('Turno'),TH('Estatus'),TH('Reporte'))))
    for registro in filas:
        if editar==1:
            if registro.guardias.estatus=='Por Aprobar':
                dato=registro.guardias.estatus
            else:
                dato=A(registro.guardias.estatus,_href=URL('guardias','cambiar_estado',vars = dict(g=registro.guardias.id)))
        elif editar==2:
            dato=A(registro.guardias.estatus,_href=URL('guardias','cambiar_estado',vars = dict(g=registro.guardias.id)))
        else:
            dato=registro.guardias.estatus
        #asigna color al dato estatus
        if registro.guardias.estatus=="Con Observaciones":
            estatus=TD(dato,_style='color:orange;')
        else:
            estatus=TD(dato,_style='color:green;')
        datos.append(TR(TD(funciones.nombre_completo(registro.guardias.id_usuario)),
                        TD(registro.guardias.fecha.strftime("%d/%m/%Y")),
                        TD(A(registro.turnos.turno,_href=URL('certificaciones','index',args=[registro.guardias.id]))),
                        estatus,
                        TD(A("Ver",_href=URL('reportes','reporte_guardia',args=[registro.guardias.id]), _target='new'))))
    return TABLE(datos,_class="table table-hover")

def presentar_datos_rotativo(filas):
    import funciones
    
    datos=[]
    estatus= None
    datos.append(THEAD(TR(TH('Fecha'),TH('Turno'),TH('Estatus'),TH('Observaciones de revisión'),TH('Revisado Por'))))
    for registro in filas:
        nestatus=registro.guardias.estatus
        if nestatus=="Con Observaciones":
            dato=A(registro.guardias.estatus,_href=URL('certificaciones','index',args=[registro.guardias.id]))
            estatus=TD(dato,_style='color:orange;')
        elif nestatus=="En Proceso":
            dato=A(registro.guardias.estatus,_href=URL('certificaciones','index',args=[registro.guardias.id]))
            estatus=TD(dato,_style='color:green;')
        else:
            dato=registro.guardias.estatus
            estatus=TD(dato,_style='color:green;')
        usuario_rev="- Sin Revisar -"
        if not registro.guardias.observaciones_rev:
            observaciones_rev=""
        else:
            observaciones_rev=registro.guardias.observaciones_rev
        if registro.guardias.id_usuario_rev:
            usuario_rev=funciones.nombre_completo(registro.guardias.id_usuario_rev)
        datos.append(TR(TD(registro.guardias.fecha.strftime("%d/%m/%Y")),
                        TD(registro.turnos.turno),
                        estatus,
                        TD(observaciones_rev),
                        TD(usuario_rev)))
    return TABLE(datos,_class="table table-hover")

def comprobar_estatus(id_guardia,id_usuario):
    query=(current.db.guardias.id==id_guardia)&(current.db.guardias.id_usuario==id_usuario)&((current.db.guardias.estatus=="Con Observaciones")|(current.db.guardias.estatus=="En Proceso"))
    filas=current.db(query).select(current.db.guardias.id)
    return filas

def enlace_cambiar_estado(id_guardia):
    import funciones
    usuario=funciones.id_usuario_actual()
    tipo_usuario_act=funciones.tipo_usuario(usuario)
    if tipo_usuario_act=="Administrador" or tipo_usuario_act=="Supervisor":
        enlace=A("Presione click aquí para cambiar estado",_href=URL('guardias','cambiar_estado',vars = dict(g=id_guardia)))
    else:
        enlace=None
    return enlace
