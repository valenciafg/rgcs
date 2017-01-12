# -*- coding: utf-8 -*-



""" database class object creation (initialization) """
if request.env.web2py_runtime_gae:                  # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
else:                                               # else use a normal relational database
    #db = SQLDB("sqlite://guardias_rotativas.db")
    #db = SQLDB("sqlite://db.db")
    db = DAL('postgres://postgres:<password>@<server>/<database>', pool_size=10)
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#Configuraciones de acceso a usuarios con LDAP

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

from gluon import current
current.db = db
#Crea todas las tablas necesarias para definir auth
#auth.settings.extra_fields['auth_user']= [Field('user_type',   requires=IS_IN_SET(['Rotativo', 'Supervisor','Administrador']), default='Rotativo')]
#auth.define_tables(username=True)

auth.settings.extra_fields['auth_user']= [Field('user_type',   requires=IS_IN_SET(['Rotativo', 'Supervisor','Administrador']), default='Rotativo'), Field('state_user', requires=IS_IN_SET(['Activo', 'Inactivo']), default ='Activo')]
auth.define_tables(username=True)

#Crea y modifica las tablas necesarias para utilizar el plugin
from plugin_ckeditor import CKEditor
ckeditor = CKEditor(db)
ckeditor.define_tables()
#ckeditor.settings.url_upload = URL(request.app, 'uploads', 'certificaciones')

import os
#
#TABLA = tipos
#
db.define_table("tipos",
    Field("desc_tipo", "string", notnull=True, default='Check'))

db.define_table("turnos",
    Field("turno",  requires=IS_IN_SET(['Mañana', 'Tarde', 'Noche'])))

db.define_table("actividades",
    Field("desc_act", "string", notnull=True, default=''),
    Field("detalle_act", "text", default=None),
    Field("estatus_act",  requires=IS_IN_SET(['Activo', 'Inactivo']), default='Activo'),
    Field("id_tipos", db.tipos))

db.define_table("checklist",
    Field("horario", "string", notnull=True, default='Cada hora'),
    Field("id_actividades", db.actividades),
    Field("id_turnos", db.turnos))

db.define_table("guardias",
    Field("fecha", "date", notnull=True),
    Field("estatus", requires=IS_IN_SET(['En Proceso','Por Aprobar','Aprobado','Con Observaciones','En Revisión']), default='En Proceso'),
    Field("turno", db.turnos),
    Field("id_usuario", db.auth_user),
    Field("observaciones", "text", default=None),
    Field("observaciones_rev", "text", default=None),
    Field("observaciones_rev_resp", "text", default=None),
    Field("id_usuario_rev", db.auth_user, default=None, required=False, notnull=False),
    Field("fecha_rev", "date", notnull=False),
    Field("id_usuario_aprob", db.auth_user, notnull=False, required=False),
    Field("fecha_aprob", "date", notnull=False),
    Field("estatus_enlaces", "upload", uploadfolder=os.path.join(request.folder,'uploads/enlaces'),default=None))
    #Field("certificacion_pdf", "string", default=''))

db.define_table("historial_eventos",
    Field("id_guardia", db.guardias),
    Field("fecha_hora", "datetime", notnull=True),
    Field("evento", "text", default=None),
    Field("id_usuario", db.auth_user, default=None, required=False, notnull=False))

db.define_table("estado_historial_eventos",
    Field("estatus",  requires=IS_IN_SET(['Activo', 'Inactivo']), default='Activo'))

db.define_table("certificaciones",
    Field("id_guardia", db.guardias),
    Field("id_checklist", db.checklist),
    Field("estatus", requires=IS_IN_SET(['Generado', 'Revisado','Aprobado','Con Observaciones','No Realizado']), default='No Realizado'),
    Field("detalle", "text", length= 160000, requires=IS_NOT_EMPTY(), default=None),
    #Field("detalle", "text", default=None, widget=ckeditor.widget),
    Field("observaciones", "text", default=None),
    Field("acciones_tomadas", "text", default=None))

db.define_table("historial_eventos_certificacion",
    Field("id_certificacion", db.certificaciones),
    Field("fecha_hora", "datetime", notnull=True),
    Field("evento", "text", default=None),
    Field("id_usuario", db.auth_user, default=None, required=False, notnull=False))

db.define_table('archivos',
		Field('id_certificacion', db.certificaciones),
		Field('titulo', type='string', label=T('Descripción'), notnull=False), # notnull=False is required
        Field('archivo', type='upload', uploadfolder=os.path.join(request.folder,'static/archivos'), autodelete=True, notnull=False))
		#Field('archivo', type='upload', uploadfolder=request.folder+'static/archivos', autodelete=True, notnull=False))
#
    #DATABASE - TABLES REQUIRES
#
db.guardias.estatus_enlaces.requires = IS_UPLOAD_FILENAME(extension='jpg|png', error_message='Ingrese un tipo de archivo válido ( jpg| png)')

""" Relations between tables (remove fields you don't need from requires) """
db.actividades.desc_act.requires=IS_LENGTH(80,error_message='El nombre de la actividad debe tener máximo 80 caracteres')

db.actividades.id_tipos.requires=IS_IN_DB( db, 'tipos.id', ' %(desc_tipo)s')
actividades_activas=db.actividades.estatus_act=='Activo'

db.checklist.id_actividades.requires=IS_IN_DB( db(actividades_activas), 'actividades.id', ' %(desc_act)s')
db.checklist.id_turnos.requires=IS_IN_DB( db, 'turnos.id', ' %(turno)s')

#db.certificaciones.id_checklist.requires=IS_IN_DB( db, 'checklist.id', ' %(horario)s %(id_actividades)s %(id_turnos)s')
db.guardias.turno.requires=IS_IN_DB( db, 'turnos.id', ' %(turno)s')
#import datetime
#db.guardias.fecha.requires=IS_DATE_IN_RANGE(format=T('%Y-%m-%d'),maximum=datetime.date(2015,1,17))
db.guardias.id_usuario_rev.requires=IS_IN_DB( db, 'auth_user.id', ' %(first_name)s')
db.guardias.id_usuario_aprob.requires=IS_IN_DB( db, 'auth_user.id', ' %(first_name)s')

db.certificaciones.id_guardia.requires=IS_IN_DB( db, 'guardias.id', ' %(id)s')
db.certificaciones.id_checklist.requires=IS_IN_DB( db, 'checklist.id', ' %(id)s')
#
#
#
db.historial_eventos.id_usuario.requires=IS_IN_DB( db, 'auth_user.id', ' %(first_name)s')
db.historial_eventos.id_guardia.requires=IS_IN_DB( db, 'guardias.id', ' %(id)s')
#db.archivos.id_certificacion.requires=IS_IN_DB( db, 'certificaciones.id', ' %(id)s')
# Configuración de acciones de autorización (no registrar, no cambiar clave, no resetear clave, etc)
auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username','profile']

# Recordar Usuario=False
auth.settings.remember_me_form = False

# Autenticación a LDAP sin recordar usuario en WEB2PY
from gluon.contrib.login_methods.ldap_auth import ldap_auth
auth.settings.login_methods = [ldap_auth(mode='ad',
       server='',
       base_dn='',
       manage_user=True,
       user_firstname_attrib='',
       user_lastname_attrib='',
       user_mail_attrib='',
       group_name_attrib = '',
       group_member_attrib = '',
       db = db)]

#Establece que no se requiera clave en la tabla interna auth_user
db.auth_user.id.requires = None
db.auth_user.password.requires = None
#auth.settings.login_next = URL('default')
auth.settings.login_next = URL("default","index")
auth.messages.invalid_login = 'Error al iniciar sesión, verifique sus datos'

def go_log(object):
    redirect(URL('default','index'))
auth.settings.login_onaccept = go_log

auth.settings.expiration = 3600*24

#auth.settings.long_expiration = 12
#auth.settings.remember_me_form = True
