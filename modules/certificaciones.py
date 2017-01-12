#!/usr/bin/env python
# coding: utf8
from gluon import *


def estatus_certificacion(guardia,checklist):
    estatus=None
    query=(current.db.certificaciones.id_guardia==guardia)&(current.db.certificaciones.id_checklist==checklist)
    filas=current.db(query).select(current.db.certificaciones.estatus)
    for fila in filas:
        estatus=fila.estatus
    return estatus

def generar_certificacion(guardia):
    certificacion=None
    query=(current.db.guardias_certificaciones.id_guardias==guardia)&(current.db.certificaciones.id==current.db.guardias_certificaciones.id_certificaciones)
    filas=current.db(query).select(current.db.certificaciones.id)
    for fila in filas:
        certificacion=fila.id
    if not certificacion:
        certificacion=current.db.certificaciones.insert(estatus="No Realizado")
        current.db.guardias_certificaciones.insert(id_guardias=guardia,
                                                   id_certificaciones=certificacion)
    return certificacion

def tipo_actividad(id_certificacion):
    tipo=none
    query=(current.db.certificaciones.id==id_certificacion)&(current.db.checklist.id==current.db.certificaciones.id_checklist)&(current.db.actividades.id==current.db.checklist.id_actividades)&(current.db.tipos.id==current.db.actividades.id_tipos)
    filas=current.db(query).select(current.db.tipo.id)
    for fila in filas:
        tipo=fila.id
    return tipo

def datos_certificacion(id_g,id_cl,id_act):
    query=(current.db.certificaciones.id_guardia==id_g)&(current.db.certificaciones.id_checklist==id_cl)&(current.db.checklist.id==current.db.certificaciones.id_checklist)&(current.db.checklist.id_actividades==id_act)&(current.db.actividades.id==current.db.checklist.id_actividades)
    filas=current.db(query).select()
    fila=None
    for fila in filas:
        pass
    return fila

def actualizar_reportes_certificaciones(id_guardia,estado):
    import reportes
    query=(current.db.certificaciones.id_guardia==id_guardia)&(current.db.checklist.id==current.db.certificaciones.id_checklist)&(current.db.actividades.id==current.db.checklist.id_actividades)
    #&((current.db.actividades.id_tipos==2)|(current.db.actividades.id_tipos==4))
    #query=(current.db.certificaciones.id_guardia==id_guardia)
    filas=current.db(query).select(current.db.certificaciones.id,current.db.certificaciones.estatus,current.db.actividades.id_tipos)
    fila=None
    for fila in filas:
        #if not(fila.estatus=="Con Observaciones"):
        #current.db(current.db.certificaciones.id == fila.certificaciones.id).update(estatus=estado)
        if fila.actividades.id_tipos==2:
            reportes.reporte_certificacion(id_guardia,fila.certificaciones.id)
        if fila.actividades.id_tipos==4:
            reportes.reporte_certificacion_img(id_guardia,fila.certificaciones.id)
    return True
    #reportes.reporte_guardia(id_guardia)
