#!/usr/bin/env python
# coding: utf8
from gluon import *
from gluon.contrib.pyfpdf import FPDF, HTMLMixin
import os
import time
import funciones
import config_reportes
class MyFPDF(FPDF, HTMLMixin):
    def cuerpo(self):
        self.cell(190,256,"",1,1)
        
'''
    GENERACION DE PDF DE REPORTE FINAL DE GUARDIA
'''
def reporte_guardia(id_guardia):
    fecha1=time.strftime("%d/%m/%Y")
    fecha2=time.strftime("%Y-%m-%d")
    
    #nturno=funciones.nombre_turno(turno)
    pdf=MyFPDF()
    titulo="Reporte de Guardia"
    
    pdf.add_page()
    pdf.set_fill_color(204,204,204)
    config_reportes.cabecera_estandar(titulo,pdf)
    query=(current.db.guardias.id==id_guardia)
    filas=current.db(query).select()
    for fila in filas:
        pass
    fguardia=fila
    config_reportes.info_guardia(fila,pdf)
    pdf.cell(155,5,"Actividad",1,0,"C",True)
    pdf.cell(35,5,"Estatus".decode("utf8").encode("latin1"),1,1,"C",True)
    query = (current.db.certificaciones.id_guardia==id_guardia)&(current.db.checklist.id==current.db.certificaciones.id_checklist)&(current.db.actividades.id==current.db.checklist.id_actividades)
    filas=current.db(query).select(current.db.actividades.desc_act,current.db.certificaciones.estatus)
    y=40
    for dato in filas:
        actividad=dato.actividades.desc_act
        pdf.set_x(10)
        if len(actividad)>120:
            alto=5
        else:
            alto=10
        pdf.multi_cell(155,alto,actividad.decode("utf8").encode("latin1"),1,0,'L')
        pdf.set_y(y)
        y=y+10
        pdf.set_x(165)
        pdf.cell(35,10,dato.certificaciones.estatus,1,1,'C',True)
    #Crea una linea desde la altura actual hasta el final de pagina (275)
    psy=275-pdf.get_y()
    pdf.cell(190,psy,"",1)
    pdf.add_page()
    pdf.cell(190,10,"Estatus de Enlaces y Equipos Caídos".decode("utf8").encode("latin1"),1,1,'C',True)
    pdf.cell(190,2,"",0,1)
    #Imprime la imagen de los enlaces en la ruta /uploads/enlaces
    img_enlaces=os.path.join(current.request.folder,"uploads","enlaces",fila.estatus_enlaces)
    pdf.image(img_enlaces,None,None,190,100)
    #multi_cell(190,5,observaciones,1,'L')
    if fila.observaciones==None:
        observaciones="Sin Observaciones"
    else:
        observaciones=fila.observaciones.decode("utf8").encode("latin1")
    pdf.multi_cell(190,5,"Observaciones: "+observaciones,1,'L')
    psy=255-pdf.get_y()
    pdf.cell(190,psy,"",1)
    config_reportes.pie_tres_estados_guardia(fguardia,pdf)
    current.response.headers['Content-Type']='application/pdf'
    return pdf.output(dest='S')

def reporte_guardia_formato():
    #nturno=funciones.nombre_turno(turno)
    pdf=MyFPDF()
    titulo="Reporte de Guardia"
    
    pdf.add_page()
    pdf.set_fill_color(204,204,204)
    config_reportes.cabecera_estandar_formato(titulo,pdf)
    config_reportes.info_guardia_formato(pdf)
    pdf.cell(155,5,"Actividad",1,0,"C",True)
    pdf.cell(35,5,"Estatus".decode("utf8").encode("latin1"),1,1,"C",True)
    
    y=40
    i=0
    for i in range(15):
        pdf.set_x(10)
        alto=10
        pdf.multi_cell(155,alto,"",1,0,'L')
        pdf.set_y(y)
        y=y+10
        pdf.set_x(165)
        pdf.cell(35,10,"",1,1,'C',True)
    #Crea una linea desde la altura actual hasta el final de pagina (275)
    psy=275-pdf.get_y()
    pdf.cell(190,psy,"",1)
    pdf.add_page()
    pdf.cell(190,10,"Estatus de Enlaces y Equipos Caídos".decode("utf8").encode("latin1"),1,1,'C',True)
    pdf.cell(190,2,"",0,1)
    #Imprime la imagen de los enlaces en la ruta /uploads/enlaces
    #img_enlaces=os.path.join(current.request.folder,"uploads","enlaces",fila.estatus_enlaces)
    #pdf.image(img_enlaces,None,None,190,100)
    psy=276-pdf.get_y()
    pdf.cell(190,230,"",1)
    config_reportes.pie_tres_estados_guardia_formato(pdf)
    current.response.headers['Content-Type']='application/pdf'
    ruta=os.path.join(current.request.folder,"static","formatos")
    nombre="/formato-guardia.pdf"
    pdf.output(ruta+nombre,dest="F")
    return pdf.output(dest='S')
'''
    GENERACION DE PDF DE CHECKLIST
'''
def checklist(turno):
    titulo="Lista de Chequeo de Actividades de Guardias Rotativas"
    cod="CÓDIGO: FO-SEI-25"
    vigen="22/08/2013"
    rev="3"
    fecha1=time.strftime("%d/%m/%Y")
    fecha2=time.strftime("%Y-%m-%d")
    nturno=funciones.nombre_turno(turno)
    
    pdf=MyFPDF()
    pdf.add_page()
    pdf.set_fill_color(204,204,204)
    config_reportes.cabecera_estandar(titulo,pdf)
    pdf.cell(20,5,"Turno:",1,0,"C")
    pdf.cell(25,5,nturno.decode("utf8").encode("latin1"),1,0,"C")
    pdf.cell(5,5,"",1,0,"C",True)
    pdf.cell(80,5,"Feriado, Sábado, Domingo".decode("utf8").encode("latin1"),1,0,"L")
    pdf.cell(35,5,"Fecha de creación:".decode("utf8").encode("latin1"),1,0,"C")
    pdf.cell(25,5,fecha1,1,1,"C")
    
    pdf.cell(155,5,"Actividad",1,0,"C",True)
    pdf.cell(35,5,"Horario de Revisión".decode("utf8").encode("latin1"),1,1,"C",True)
    query=(current.db.checklist.id_turnos==turno)&(current.db.actividades.id==current.db.checklist.id_actividades)
    filas=current.db(query).select(current.db.checklist.horario,
                                   current.db.actividades.desc_act,
                                   orderby=current.db.checklist.horario|current.db.checklist.id)
    horario=None
    y=40
    for fila in filas:
        horario=fila.checklist.horario
        actividad=fila.actividades.desc_act
        pdf.set_x(10)
        if len(actividad)>120:
            alto=5
        else:
            alto=10
        #actividad=actividad+" ==="+str(len(actividad))
        pdf.multi_cell(155,alto,actividad.decode("utf8").encode("latin1"),1,'L')
        pdf.set_y(y)
        y=y+10
        pdf.set_x(165)
        pdf.cell(35,10,horario,1,1,'C')
    config_reportes.pie_dos_estados(pdf)
    current.response.headers['Content-Type']='application/pdf'
    ruta=os.path.join(current.request.folder,"static","checklist")
    nombre="/"+str(turno)+"-checklist.pdf"
    #pdf.output(ruta+nombre,dest="F")
    return pdf.output(nombre,dest='S')

def checklist_formato():
    titulo="Lista de Chequeo de Actividades de Guardias Rotativas"
    cod="CÓDIGO: FO-SEI-25"
    vigen=""
    rev=""

    pdf=MyFPDF()
    pdf.add_page()
    pdf.set_fill_color(204,204,204)
    config_reportes.cabecera_estandar_formato(titulo,pdf)
    pdf.cell(20,5,"Turno:",1,0,"C")
    pdf.cell(25,5,"",1,0,"C")
    pdf.cell(5,5,"",1,0,"C",True)
    pdf.cell(80,5,"Feriado, Sábado, Domingo".decode("utf8").encode("latin1"),1,0,"L")
    pdf.cell(35,5,"Fecha de creación:".decode("utf8").encode("latin1"),1,0,"C")
    pdf.cell(25,5," ",1,1,"C")
    
    pdf.cell(155,5,"Actividad",1,0,"C",True)
    pdf.cell(35,5,"Horario de Revisión".decode("utf8").encode("latin1"),1,1,"C",True)

    y=40
    i=0
    for i in range(15):
        pdf.set_x(10)
        alto=10
        #actividad=actividad+" ==="+str(len(actividad))
        pdf.multi_cell(155,alto,"",1,'L')
        pdf.set_y(y)
        y=y+10
        pdf.set_x(165)
        pdf.cell(35,10,"",1,1,'C')
    config_reportes.pie_dos_estados(pdf)
    current.response.headers['Content-Type']='application/pdf'
    ruta=os.path.join(current.request.folder,"static","formato")
    nombre="formato-checklist.pdf"
    pdf.output(ruta+nombre,dest="F")
    return pdf.output(dest='S')
'''
    GENERACION DE PDF DE CERTIFICACIONES (SOLO TEXTO)

'''
def reporte_certificacion(id_guardia,id_certificacion):
    import guardias
    fecha1=time.strftime("%d/%m/%Y")
    fecha2=time.strftime("%Y-%m-%d")

    #nturno=funciones.nombre_turno(turno)
    pdf=MyFPDF()
    pdf.add_page()

    temp=MyFPDF()
    temp.add_page()

    titulo="Reporte de guardia"
    pdf.set_fill_color(204,204,204)
    #Consulta de nombre de Actividad
    query=(current.db.certificaciones.id==int(id_certificacion))&(current.db.checklist.id==current.db.certificaciones.id_checklist)&(current.db.actividades.id==current.db.checklist.id_actividades)
    filas=current.db(query).select(current.db.actividades.desc_act)
    for fila in filas:
        pass
    fact=fila
    titulo=fact.desc_act
    config_reportes.cabecera_estandar(titulo,pdf)
    config_reportes.cabecera_estandar(titulo,temp)
    query=(current.db.guardias.id==id_guardia)
    filas=current.db(query).select()
    for fila in filas:
        pass
    fguardia=fila
    config_reportes.info_guardia(fguardia,pdf)
    config_reportes.info_guardia(fguardia,temp)

    query=(current.db.certificaciones.id==id_certificacion)
    filas=current.db(query).select()
    for fila in filas:
        pass
    fcerti=fila
    
    pdf.set_font('Arial','',10)
    temp.set_font('Arial','',10)
    pdf.cell(190,5,"Detalle de las Actividades Realizadas".decode("utf8").encode("latin1"),1,1,"L")
    temp.cell(190,5,"Detalle de las Actividades Realizadas:".decode("utf8").encode("latin1"),1,1,"L")
    
    #fcerti.detalle=fcerti.detalle.replace("/proyecto/static/certificaciones/","/home/www-data/web2py/applications/proyecto/static/certificaciones/")
    if fcerti.observaciones:
        observaciones="Observaciones: "+fcerti.observaciones.decode("utf8").encode("latin1", 'ignore')
    else:
        observaciones="Observaciones: "
    if fcerti.acciones_tomadas:
        acciones="Acciones Tomadas: "+fcerti.acciones_tomadas.decode("utf8").encode("latin1", 'ignore')
    else:
        acciones="Acciones Tomadas: "
    #Fila hasta final de cabecera
    y1=pdf.get_y()
    y11=temp.get_y() #Debe ser 40 (cabecera = 30 + margen superior = 10)
    long = "cabecera "+str(y1)
    temp.set_font('courier','',8)
    temp.multi_cell(190,5,fcerti.detalle,1,'L')
    long = long+"fin detalle: "+str(temp.get_y())
    long_detalle=temp.get_y()
    temp.set_font('Arial','',8)
    temp.multi_cell(190,5,observaciones,1,'L')
    long = long+"fin observaciones: "+str(temp.get_y())
    temp.multi_cell(190,5,acciones,1,'L')
    long = long+"fin acciones: "+str(temp.get_y())
    long_final=temp.get_y()
    longs=0
    if long_final<255:
        longs=long_final
        while(longs<255):
            fcerti.detalle = fcerti.detalle + "\n"
            longs=longs+5
    elif long_final>250:
        longs=long_final
        pare=(245/5)+((275-longs)/5)
        i=0
        while(i<pare):
            fcerti.detalle = fcerti.detalle + "\n"
            i=i+1
    #long=long+"long_final="+str(long_final)+"longs="+str(longs)

    pdf.set_font('courier','',8)
    pdf.multi_cell(190,5,fcerti.detalle,1,'L')
    pdf.set_font('Arial','',8)

    pdf.multi_cell(190,5,observaciones,1,'L')
    pdf.multi_cell(190,5,acciones,1,'L')
    y2=pdf.get_y()
    y22=temp.get_y()
    #pdf.multi_cell(190,5,"pare: "+str(pare),1,'L')
    #pdf.multi_cell(190,5,str(long_final)+long,1,'L')
    #pdf.multi_cell(190,5,str(y1),1,'L')
    #pdf.multi_cell(190,5,str(y11),1,'L')
    #pdf.multi_cell(190,5,long,1,'L')
    #pdf.multi_cell(190,5,str(y22),1,'L')
    #PIE DE PAGINA
    config_reportes.pie_tres_estados_guardia(fguardia,pdf)
    current.response.headers['Content-Type']='application/pdf'
    ruta=os.path.join(current.request.folder,"static","certificaciones","docs")
    nombre="/"+str(guardias.fecha_guardia(id_guardia))+"-"+str(id_certificacion)+"-certificacion.pdf"
    pdf.output(ruta+nombre,dest="F")
    return pdf.output(dest='S')
    #return dict(pdf=str(XML(fcerti.detalle, sanitize=False)))
    
def reporte_certificacion_formato():
    pdf=MyFPDF()
    pdf.add_page()

    titulo="Formato único de certificación de actividades"
    pdf.set_fill_color(204,204,204)
    
    config_reportes.cabecera_estandar_formato(titulo,pdf)
    config_reportes.info_guardia_formato(pdf)
    pdf.set_font('Arial','',10)
    pdf.cell(190,5,"Detalle de las Actividades Realizadas".decode("utf8").encode("latin1"),1,1,"L")

    pdf.set_font('courier','',8)
    pdf.multi_cell(190,205,"",1,'L')
    pdf.set_font('Arial','',8)

    pdf.multi_cell(190,5,"Observaciones:",1,'L')
    pdf.multi_cell(190,5,"Acciones tomadas:",1,'L')

    #PIE DE PAGINA
    config_reportes.pie_tres_estados_guardia_formato(pdf)
    #config_reportes.pie_dos_estados(pdf)
    current.response.headers['Content-Type']='application/pdf'
    ruta=os.path.join(current.request.folder,"static","formatos")
    nombre="/formato-certificacion.pdf"
    pdf.output(ruta+nombre,dest="F")
    return pdf.output(dest='S')
'''
    GENERACION DE PDF DE CERTIFICACIONES (SOLO IMAGENES)

'''
def reporte_certificacion_img(id_guardia,id_certificacion):
    import guardias
    fecha1=time.strftime("%d/%m/%Y")
    fecha2=time.strftime("%Y-%m-%d")

    #nturno=funciones.nombre_turno(turno)
    pdf=MyFPDF()
    pdf.add_page()

    temp=MyFPDF()
    temp.add_page()

    titulo="Reporte de guardia"
    pdf.set_fill_color(204,204,204)

    #Consulta de nombre de Actividad
    query=(current.db.certificaciones.id==id_certificacion)&(current.db.checklist.id==current.db.certificaciones.id_checklist)&(current.db.actividades.id==current.db.checklist.id_actividades)
    filas=current.db(query).select(current.db.actividades.desc_act)
    for fila in filas:
        pass
    fact=fila
    titulo=fact.desc_act
    config_reportes.cabecera_estandar(titulo,pdf)
    config_reportes.cabecera_estandar(titulo,temp)

    #Consulta datos de la guardia
    query=(current.db.guardias.id==id_guardia)
    filas=current.db(query).select()
    for fila in filas:
        pass
    fguardia=fila
    config_reportes.info_guardia(fguardia,pdf)
    config_reportes.info_guardia(fguardia,temp)

    #Consulta datos de la certificacion
    query=(current.db.certificaciones.id==id_certificacion)
    filas=current.db(query).select()
    for fila in filas:
        pass
    fcerti=fila

    #Consulta datos de los archivos (IMAGENES)
    query = (current.db.archivos.id_certificacion==id_certificacion)
    filas=current.db(query).select()
    import imagenes
    pdf.set_font('Arial','',10)
    for fila in filas:
        desc_archi=fila.titulo.decode("utf8").encode("latin1", 'ignore')
        if not desc_archi:
            desc_archi="Imagen sin descripción".decode("utf8").encode("latin1", 'ignore')
        pdf.cell(190,5,"",0,1)
        pdf.multi_cell(190,5,desc_archi,1,'L',True)
        ruta_img=ruta=os.path.join(current.request.folder,"static","archivos",fila.archivo)
        #imagenes.thumbnail(ruta_img)
        pdf.image(ruta_img,None,None,190,100)

    config_reportes.pie_tres_estados_guardia(fguardia,pdf)
    current.response.headers['Content-Type']='application/pdf'
    ruta=os.path.join(current.request.folder,"static","certificaciones","docs")
    nombre="/"+str(guardias.fecha_guardia(id_guardia))+"-"+str(id_certificacion)+"-certificacion.pdf"
    pdf.output(ruta+nombre,dest="F")
    return pdf.output(dest='S')
