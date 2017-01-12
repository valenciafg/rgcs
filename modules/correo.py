#!/usr/bin/env python
# coding: utf8
from gluon import *

def confirmar_guardia_correo(id):
    #initialize = local_import('initialize')
    #initialize.fillup(db, response)
    enviado=None
    from gluon.tools import Mail
    import guardias
    import os
    usuario,fecha,turno,estatus,correo=guardias.datos_guardia_correo(id)
    if not correo:
        correo='certificaciones@seguroscaroni.com'
    contenido="<b>Realizada por:</b> "+usuario+"<br><b>Fecha: </b>"+fecha+"<br><b>Turno: </b>"+turno+"<br><b>Estatus actual: </b>"+estatus
    mail = Mail()
    mail.settings.server = '<server address>'
    mail.settings.sender = '<email>'
    mail.settings.login = None
    asunto="Ha sido generada una nueva guardia"
    adjuntos= []
    #Obtiene el PDF del reporte de guardia
    pdf_guardia=str(id)+"-guardia.pdf"
    path=os.path.join(current.request.folder, 'static/guardias',pdf_guardia)
    #path="/home/www-data/web2py/applications/guardias/static/guardias/"+pdf_guardia
    if os.path.isfile(path):
        adjuntos.append(mail.Attachment(path, content_id='reporte_guardia'))

    #Obtiene la imagen de estado del Enlaces si existe
    registro=current.db.guardias(id)
    if registro.estatus_enlaces:
        path=os.path.join(current.request.folder, 'uploads/enlaces',registro.estatus_enlaces)
        #path="/home/www-data/web2py/applications/guardias/uploads/enlaces/"+registro.estatus_enlaces
        if os.path.isfile(path):
            adjuntos.append(mail.Attachment(path, content_id='enlaces'))
    #Comprobar si hay observaciones
    if registro.observaciones:
        obs=registro.observaciones
        obs=obs.replace("\n","<br>")
        contenido=contenido+'<br><b>Obervaciones:</b><br>'+obs
    #contenido='<html>'+contenido+'<br><b>Enlaces caídos, sin electricidad, servidores alarmados: </b><br><img src="cid:enlaces" /><br><b><a href="'+url+'">Reviar aquí:</a></b></><br></html>'
    contenido='<html>'+contenido+'<br><b>Enlaces caídos, sin electricidad, servidores alarmados: </b><br><img src="cid:enlaces" /><br></html>'
    #url='%s://%s%s' % (request.env.wsgi_url_scheme, request.env.http_host, '/certificaciones/index/'+str(id))
    #str(URL('certificaciones','index',args=[id]))
    enviado=mail.send(to=['rotativo@seguroscaroni.com'],
                      subject = asunto,
                      message = contenido,
                      attachments = adjuntos)
    return enviado

def cambio_estado_guardia_correo(id,usr,observacion):
    enviado=None
    from gluon.tools import Mail
    import guardias
    usuario,fecha,turno,estatus,correo=guardias.datos_guardia_correo(id)
    if not correo:
        correo='certificaciones@seguroscaroni.com'
    mail = Mail()
    mail.settings.server = '<server address>'
    mail.settings.sender = '<email>'
    mail.settings.login = None
    asunto="Se ha cambiado el estatus de una guardia"
    contenido="<html><b>Guardia realizada por: </b>"+usuario+"<br><b>Fecha: </b>"+fecha+"<br><b>Turno: </b>"+turno+"<br><b>Estatus actual:</b> "+estatus+"<br><b>Observaciones de revisión: </b><br>"+observacion+"<br><b>Estatus cambiado por: </b>"+usr+"</html>"
    enviado=mail.send(to=['rotativo@seguroscaroni.com'],
              subject=asunto,
              message=contenido)
    return enviado
