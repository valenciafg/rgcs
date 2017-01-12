#!/usr/bin/env python
# coding: utf8
from gluon import *

def tipo_actividad(id):
    tipo=None
    query = (current.db.actividades.id==id)&(current.db.tipos.id==current.db.actividades.id_tipos)
    filas=current.db(query).select(current.db.tipos.desc_tipo)
    for fila in filas:
        tipo=fila.desc_tipo
    return tipo

def id_tipo_actividad(id):
    id_tipo=None
    query = (current.db.actividades.id==id)&(current.db.tipos.id==current.db.actividades.id_tipos)
    filas=current.db(query).select(current.db.tipos.id)
    for fila in filas:
        id_tipo=fila.id
    return id_tipo
