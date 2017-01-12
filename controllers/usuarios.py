# coding: utf8
# intente algo como
@auth.requires_login()
def index():
    import funciones
    id_usuario_act = funciones.id_usuario_actual()
    lusuarios=listar_usuarios(id_usuario_act)
    return dict(lusuarios=lusuarios)

def listar_usuarios(id):
    import funciones
    if funciones.tipo_usuario(funciones.id_usuario_actual())=='Administrador':
    #if funciones.tipo_usuario(funciones.id_usuario_actual())=='Rotativo':
    
        sw=1
    else:
        sw=0
    query=(db.auth_user.id!=id)
    #filas=db(query).select(db.auth_user.id,db.auth_user.username,db.auth_user.first_name,db.auth_user.email,db.auth_user.last_name,db.auth_user.user_type)
    #datos=[]
     
    filas=db(query).select(db.auth_user.id,db.auth_user.username,db.auth_user.first_name,db.auth_user.email,db.auth_user.last_name,db.auth_user.user_type,db.auth_user.state_user)
    datos=[]
    datos.append(THEAD(TR(TH('#'),TH('Usuario'),TH('Nombre y Apellido'),TH('Correo'),TH('Cargo'),TH('Tipo'),TH('Estado'))))
    cont=1
    for registro in filas:
        if sw==1:
            enlace=A(registro.user_type,_href=URL('usuarios','editar_tipo',vars = dict(id=registro.id)))
        if sw==1:
            enlace_1=A(registro.state_user,_href=URL('usuarios','editar_tipo_1',vars = dict(id=registro.id)))
        else:
            enlace=registro.user_type
            enlace_1=registro.state_user
        datos.append(TR(TD(cont),
                        TD(registro.username),
                        TD(registro.first_name),
                        TD(registro.email),
                        TD(registro.last_name),
                        TD(enlace),
                        TD(enlace_1)))
        cont=cont+1
    return TABLE(datos,_class="table table-hover")
@auth.requires_login()
def editar_tipo():
    import funciones
    id_user = request.vars.id or redirect(URL('usuarios','index'))
    nombre=funciones.nombre_completo(id_user)

       # ftipo = SQLFORM.factory(Field("user_type", db.auth_user,requires=IS_IN_SET(['Rotativo', 'Supervisor','Administrador']), default='Rotativo', label=nombre),
                         #  submit_button="Modificar Usuario"
    ftipo = SQLFORM.factory(Field("user_type", db.auth_user,requires=IS_IN_SET(['Rotativo', 'Supervisor','Administrador']), default='Rotativo', label=nombre),
                          submit_button="Modificar Usuario")
    
  
    if ftipo.process().accepted:
        db(db.auth_user.id==id_user).update(user_type=ftipo.vars.user_type)
        msj="Usuario "+nombre+" fue cambiado al usuario "+ftipo.vars.user_type
        session.flash = msj
        redirect(URL('usuarios','index'))
    return dict(ftipo=ftipo)

def editar_tipo_1(): 
    import funciones
    id_user = request.vars.id or redirect(URL('usuarios','index'))
    nombre=funciones.nombre_completo(id_user)
    
    ftipo1 = SQLFORM.factory(Field("state_user", db.auth_user,requires=IS_IN_SET(['Activo', 'Inactivo']), default='Activo', label=nombre),
                          submit_button="Modificar estado")

    if ftipo1.process().accepted:

        db(db.auth_user.id==id_user).update(state_user=ftipo1.vars.state_user)
        msj="Usuario "+nombre+" fue cambiado al usuario "+ftipo1.vars.state_user
        session.flash = msj
        redirect(URL('usuarios','index'))
    return dict(ftipo1=ftipo1)
