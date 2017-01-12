#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

def estado_logs():
    estado=None
    query=(current.db.estado_historial_eventos.id==1)
    filas=current.db(query).select(current.db.estado_historial_eventos.estatus)
    for fila in filas:
        estado=fila.estatus
    return estado
