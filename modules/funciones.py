#!/usr/bin/env python
# coding: utf8
from gluon import *

def nombre_usuario_actual():
    usuario_actual=None
    usuario=current.session.usuario
    query=(current.db.auth_user.id==usuario)
    result=current.db(query).select(current.db.auth_user.username)
    for row in result:
        usuario_actual=row.username
    return usuario_actual

def nombre_usuario(id):
    nombre_usuario=None
    query=(current.db.auth_user.id==id)
    result=current.db(query).select(current.db.auth_user.username)
    for row in result:
        nombre_usuario=row.username
    return nombre_usuario

def nombre_completo(id):
    nombre_usuario=None
    query=(current.db.auth_user.id==id)
    result=current.db(query).select(current.db.auth_user.first_name)
    for row in result:
        nombre_usuario=row.first_name
    return nombre_usuario

def id_usuario_actual():
    return current.session.usuario

def tipo_usuario(id):
    tipo=None
    query=(current.db.auth_user.id==id)
    result=current.db(query).select(current.db.auth_user.user_type)
    for row in result:
        tipo=row.user_type
    return tipo

def correo_usuario(id):
    correo=None
    query=(current.db.auth_user.id==id)
    result=current.db(query).select(current.db.auth_user.email)
    for row in result:
        correo=row.email
    return correo

def nombre_turno(id):
    nombre=None
    query=(current.db.turnos.id==id)
    result=current.db(query).select(current.db.turnos.turno)
    for row in result:
        nombre=row.turno
    return nombre
