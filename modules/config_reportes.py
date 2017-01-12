#!/usr/bin/env python
# coding: utf8
from gluon import *
import os
import funciones

def cabecera_estandar(titulo,pdf):
    cod="CÓDIGO: FO-SEI-25"
    vigen="22/08/2013"
    rev="3"
    #Logo Seguros Caroní, S.A.
    logo=os.path.join(current.request.folder,"static","images","sc.png")
    pdf.image(logo,10,15,60)
    pdf.set_font('Arial','B',12)
    #Celda donde va el logo
    pdf.cell(60,20,"",1)
    #Titulo del reporte
    if len(titulo)<39:
        titulo=titulo+"\n "
    pdf.multi_cell(110,10,titulo.decode("utf8").encode("latin1"),1,'C')
    #pdf.cell(90,20,titulo.decode("utf8").encode("latin1"),1,0,'C')
    pdf.set_font('Arial','',8)
    #Formato del Reporte
    #pdf.set_y(10)
    #pdf.set_x(160)
    #pdf.cell(40,5,cod.decode("utf8").encode("latin1"),1,2,'C')
    #pdf.cell(20,5,"VIGENCIA",1,0,'C')
    #pdf.cell(20,5,"N° REVISIÓN".decode("utf8").encode("latin1"),1,1,'C')
    #pdf.cell(150,5,"",0)
    #pdf.cell(20,5,vigen,1,0,'C')
    #pdf.cell(20,5,rev,1,1,'C')
    #pdf.cell(150,5,"",0)
    #Numero de paginas
    #txt = 'PÁGINA %s / %s' % (pdf.page_no(), pdf.alias_nb_pages())
    #pdf.cell(40,5,txt.decode("utf8").encode("latin1"),1,1,'C')
    pdf.set_y(10)
    pdf.set_x(180)
    #Numero de paginas
    pdf.cell(20,10,"N° PÁGINAS".decode("utf8").encode("latin1"),1,1,'C')
    #txt = 'PÁGINA %s / %s' % (pdf.page_no(), pdf.alias_nb_pages())
    txt = '%s' % (pdf.alias_nb_pages())
    pdf.set_y(20)
    pdf.set_x(180)
    pdf.cell(20,10,txt.decode("utf8").encode("latin1"),1,1,'C')
    
def cabecera_estandar_formato(titulo,pdf):
    cod="CÓDIGO: "
    vigen=""
    rev=""
    #Logo Seguros Caroní, S.A.
    logo=os.path.join(current.request.folder,"static","images","sc.png")
    pdf.image(logo,10,15,60)
    pdf.set_font('Arial','B',12)
    #Celda donde va el logo
    pdf.cell(60,20,"",1)
    #Titulo del reporte
    if len(titulo)<39:
        titulo=titulo+"\n "
    pdf.multi_cell(110,10,titulo.decode("utf8").encode("latin1"),1,'C')
    pdf.set_font('Arial','',8)
    #Formato del Reporte
    pdf.set_y(10)
    pdf.set_x(180)
    #Numero de paginas
    pdf.cell(20,10,"N° PÁGINAS".decode("utf8").encode("latin1"),1,1,'C')
    #txt = 'PÁGINA %s / %s' % (pdf.page_no(), pdf.alias_nb_pages())
    txt = '%s' % (pdf.alias_nb_pages())
    pdf.set_y(20)
    pdf.set_x(180)
    pdf.cell(20,10,txt.decode("utf8").encode("latin1"),1,1,'C')
    
def pie_tres_estados_guardia(fila,pdf):
    pdf.set_y(255)
    pdf.set_font('Arial','B',10)
    yy=pdf.get_y()
    pdf.cell(63.3,5,"ELABORADO POR",1,0,'C')
    pdf.cell(63.3,5,"REVISADO POR",1,0,'C')
    pdf.cell(63.3,5,"APROBADO POR",1,1,'C')
    #Nombre de quien creo la guardia
    pdf.set_font('Arial','',7)
    pdf.cell(24,5,"Nombre y Apellido:","L",0)
    pdf.set_font('Arial','',7)
    pdf.cell(39.3,5,funciones.nombre_completo(fila.id_usuario).decode("utf8").encode("latin1"),"R",0)
    #Nombre de quien reviso la guardia
    pdf.set_font('Arial','',7)
    pdf.cell(24,5,"Nombre y Apellido:","L",0)
    pdf.set_font('Arial','',7)
    if (fila.id_usuario_rev==None) or (fila.estatus == "Con Observaciones"):
        usr_rev=""
    else:
        usr_rev=funciones.nombre_completo(fila.id_usuario_rev).decode("utf8").encode("latin1")
        
    pdf.cell(39.3,5,usr_rev,"R",0)
    #Nombre de quien aprobo la guardia
    pdf.set_font('Arial','',7)
    pdf.cell(24,5,"Nombre y Apellido:","L",0)
    pdf.set_font('Arial','',7)
    
    if (fila.id_usuario_aprob==None) or (fila.estatus == "Con Observaciones"):
        usr_aprob=""
    else:
        usr_aprob=funciones.nombre_completo(fila.id_usuario_aprob).decode("utf8").encode("latin1")
    pdf.cell(39.3,5,usr_aprob,"R",1)
    #Fecha de creacion
    pdf.set_font('Arial','',8)
    pdf.cell(13,5,"Fecha:","L",0)
    pdf.cell(50.3,5,str(fila.fecha.strftime("%d/%m/%Y")),"R",0)
    #Fecha de revision
    pdf.cell(13,5,"Fecha:","L",0)
    if fila.fecha_rev==None:
        frev=""
    else:
        frev=str(fila.fecha_rev.strftime("%d/%m/%Y"))
    pdf.cell(50.3,5,frev,"R",0)
    #Fecha de aprobacion
    pdf.cell(13,5,"Fecha:","L",0)
    if fila.fecha_aprob==None:
        faprob=""
    else:
        faprob=str(fila.fecha_aprob.strftime("%d/%m/%Y"))
    pdf.cell(50.3,5,faprob,"R",1)
    pdf.cell(13,5,"Firma:","LB",0)
    pdf.cell(50.3,5,"","RB",0)
    pdf.cell(13,5,"Firma:","LB",0)
    pdf.cell(50.3,5,"","RB",0)
    pdf.cell(13,5,"Firma:","LB",0)
    pdf.cell(50.3,5,"","RB",1)
    
def pie_tres_estados_guardia_formato(pdf):
    pdf.set_y(255)
    pdf.set_font('Arial','B',10)
    yy=pdf.get_y()
    pdf.cell(63.3,5,"ELABORADO POR",1,0,'C')
    pdf.cell(63.3,5,"REVISADO POR",1,0,'C')
    pdf.cell(63.3,5,"APROBADO POR",1,1,'C')
    #Nombre de quien creo la guardia
    pdf.set_font('Arial','',9)
    pdf.cell(28,5,"Nombre y Apellido:","L",0)
    pdf.set_font('Arial','',7.5)
    pdf.cell(35.3,5,"","R",0)
    #Nombre de quien reviso la guardia
    pdf.set_font('Arial','',9)
    pdf.cell(28,5,"Nombre y Apellido:","L",0)
    pdf.set_font('Arial','',7.5) 
    pdf.cell(35.3,5,"","R",0)
    #Nombre de quien aprobo la guardia
    pdf.set_font('Arial','',9)
    pdf.cell(28,5,"Nombre y Apellido:","L",0)
    pdf.set_font('Arial','',7.5)
    pdf.cell(35.3,5,"","R",1)
    #Fecha de creacion
    pdf.set_font('Arial','',9)
    pdf.cell(13,5,"Fecha:","L",0)
    pdf.cell(50.3,5,"","R",0)
    #Fecha de revision
    pdf.cell(13,5,"Fecha:","L",0)
    pdf.cell(50.3,5,"","R",0)
    #Fecha de aprobacion
    pdf.cell(13,5,"Fecha:","L",0)
    pdf.cell(50.3,5,"","R",1)
    pdf.cell(13,5,"Firma:","LB",0)
    pdf.cell(50.3,5,"","RB",0)
    pdf.cell(13,5,"Firma:","LB",0)
    pdf.cell(50.3,5,"","RB",0)
    pdf.cell(13,5,"Firma:","LB",0)
    pdf.cell(50.3,5,"","RB",1)

def pie_dos_estados(pdf):
    pdf.set_y(-45)
    pdf.set_font('Arial','B',11)
    pdf.cell(95,6,"REVISADO POR",1,0,'C')
    pdf.cell(95,6,"APROBADO POR",1,1,'C')
    pdf.set_font('Arial','',9)
    
    pdf.cell(43,6,"Nombre y Apellido:","L",0)
    pdf.cell(52,6,"","R",0)
    pdf.cell(43,6,"Nombre y Apellido:","L",0)
    pdf.cell(52,6,"","R",1)
    
    pdf.cell(21,6,"Fecha:","L",0)
    pdf.cell(74,6,"","R",0)
    pdf.cell(21,6,"Fecha:","L",0)
    pdf.cell(74,6,"","R",1)
    
    pdf.cell(21,6,"Firma:","LB",0)
    pdf.cell(74,6,"","RB",0)
    pdf.cell(21,6,"Firma:","LB",0)
    pdf.cell(74,6,"","RB",1)
    
def info_guardia(fila, pdf):
    pdf.cell(22,5,"Elaborado por:",1,0,"C")
    pdf.cell(45,5,funciones.nombre_completo(fila.id_usuario).decode("utf8").encode("latin1"),1,0,"C",True)
    pdf.cell(28,5,"Fecha de creación:".decode("utf8").encode("latin1"),1,0,"C")
    pdf.cell(20,5,str(fila.fecha.strftime("%d/%m/%Y")),1,0,"C",True)
    pdf.cell(10,5,"Turno:",1,0,"C")
    pdf.cell(20,5,funciones.nombre_turno(fila.turno).decode("utf8").encode("latin1"),1,0,"C",True)
    pdf.cell(15,5,"Estatus",1,0,"C")
    pdf.cell(30,5,fila.estatus.decode("utf8").encode("latin1"),1,1,"C",True)
def info_guardia_formato(pdf):
    pdf.cell(25,5,"Elaborado por:",1,0,"C")
    pdf.cell(40,5,"",1,0,"C",True)
    pdf.cell(30,5,"Fecha de creación:".decode("utf8").encode("latin1"),1,0,"C")
    pdf.cell(20,5,"",1,0,"C",True)
    pdf.cell(10,5,"Turno:",1,0,"C")
    pdf.cell(20,5,"",1,0,"C",True)
    pdf.cell(15,5,"Estatus",1,0,"C")
    pdf.cell(30,5,"",1,1,"C",True)
