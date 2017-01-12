# coding: utf8
# intente algo como
def index(): 
    redirect(URL('default','index'))

def adjuntar():
    form=SQLFORM.factory(db.archivos)
    if form.process().accepted:
        db.archivos.insert(adjunto=form.vars.adjunto)
        session.flash="guardado"
    return dict(form=form)
    
def pdf_checklist():
    turno = request.vars.t or redirect(URL('default','index'))
    import reportes
    pdf=reportes.checklist(turno)
    return pdf

def pdf_checklist_formato():
    import reportes
    pdf=reportes.checklist_formato()
    return pdf

def pdf_guardia():
    #guardia = request.vars.g or redirect(URL('default','index'))
    import reportes
    pdf=reportes.reporte_guardia_formato()
    return pdf
def pdf_certificacion():
    import reportes
    pdf=reportes.reporte_certificacion_formato()
    return pdf
def reporte_guardia():
    guardia = request.args(0) or redirect(URL('default','index'))
    import reportes
    pdf=reportes.reporte_guardia(guardia)
    return pdf
def reporte_certificacion():
    guardia = request.args(0) or redirect(URL('default','index'))
    certificacion = request.args(1) or redirect(URL('default','index'))
    import reportes
    pdf=reportes.reporte_certificacion(guardia,certificacion)
    return pdf
def reporte_certificacion_img():
    guardia = request.args(0) or redirect(URL('default','index'))
    certificacion = request.args(1) or redirect(URL('default','index'))
    import reportes
    pdf=reportes.reporte_certificacion_img(guardia,certificacion)
    return pdf
