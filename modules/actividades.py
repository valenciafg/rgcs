#!/usr/bin/env python
# coding: utf8
from gluon import *

def nombre_actividad(id):
    nombre=None
    query=(current.db.actividades.id==id)
    filas=current.db(query).select(current.db.actividades.desc_act)
    for fila in filas:
        nombre=fila.desc_act
    return nombre
def div_detalle_actividad(id):
    detalle=None
    query=(current.db.actividades.id==id)
    filas=current.db(query).select(current.db.actividades.detalle_act)
    for fila in filas:
        #detalle=fila.detalle_act
        if fila.detalle_act:
            detalle=DIV(H4("Detalle"),P(fila.detalle_act),_class='bs-callout bs-callout-info')
        else:
            detalle=""
    return detalle
