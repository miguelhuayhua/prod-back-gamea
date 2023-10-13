# base de datos
from sqlalchemy import desc
from database.conexion import session
from models.Usuario import Usuario
from models.AccionesUsuario import AccionesUsuario
from models.AccesoUsuario import Acceso
import os
from sqlalchemy import func


import bcrypt
async def insertUsuario(data):
    file = data.get('fotografia')
    file_path = os.path.join(file.filename)
    file_path = file_path.replace(' ','')
    file_path = file_path.lower()
    with open("public/usersimg/"+ file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
    usuario_name = data.get('usuario')
    password = data.get('password')
    id_persona = data.get('id_persona')
    usuario = Usuario(id_usuario = Usuario.generate_id(), usuario = usuario_name,
                      password = password , fotografia = f"/static/images/{file_path}", 
                      id_persona = id_persona)
    session.add(usuario)
    session.commit()
    return usuario.id_usuario

async def verifyUsuario(usuario):
    result = session.query(Usuario).filter_by(usuario = usuario.get('usuario')).first()
    if(usuario.get('id_usuario')==""):
        return result
    else:
        try:
            usuarioExist = session.query(Usuario).filter_by(id_usuario = usuario.get('id_usuario')).first()
            if(usuarioExist.usuario == result.usuario):
                return None
            else:
                return usuarioExist
        except Exception as e:
            print(e)

async def listarUsuarios():
    return session.query(Usuario).order_by(desc(Usuario.id_usuario)).all()

async def loggedUsuario(id_usuario):
    try:
       
        return True
    except Exception as e:
        print(e)



async def getUsuario(id_usuario)->Usuario:
    usuario = session.query(Usuario).filter_by(id_usuario = id_usuario).first()
    return usuario


async def cambiarEstado(id_usuario):
    usuario = session.query(Usuario).filter_by(id_usuario = id_usuario).first()
    if usuario.estado ==0:
        usuario.estado = 1
    else :
        usuario.estado= 0
    session.commit()
    return True

async def modificarUsuario(usuario):
    id_usuario = usuario.get('id_usuario')
    usuarioUpdated = session.query(Usuario).filter_by(id_usuario = id_usuario).first()
    file = usuario.get('fotografia')
    print(file)
    if(file != 'null' and file):
        print('entra')
        file_path = os.path.join(file.filename)
        file_path = file_path.replace(' ','')
        file_path = file_path.lower()
        with open("public/usersimg/"+ file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        usuarioUpdated.fotografia = f"/static/images/{file_path}"
    if(usuario.get('password')!='' and usuario.get('password')):
        usuarioUpdated.password = usuario.get('password')
    usuarioUpdated.usuario = usuario.get('usuario')
    session.commit()
    return usuarioUpdated.id_usuario

async def getAccionesById(id_usuario):
    return session.query(AccionesUsuario).filter_by(id_usuario = id_usuario).all()

async def getAccesosById(id_usuario):
    horas = session.execute(f"SELECT * FROM total_horas_usuario('{id_usuario}')").first()
    accesos_usuario = session.query(Acceso).filter_by(id_usuario = id_usuario).all()
    return {"horas":horas[0], "accesos_usuario":accesos_usuario}


async def getByNameAndPassword(usuario):    
    try:
        usuario_name = usuario.get('usuario')+"".strip()
        password = usuario.get('password')+"".strip()
        if(usuario_name and password):
            b_password = password.encode('utf-8')
            result = session.query(Usuario).filter_by(usuario = usuario_name).first()
            if bcrypt.checkpw(b_password,result.password.encode('utf-8')):
                acceso = Acceso(id_usuario = result.id_usuario , id_acceso = Acceso.generate_id())
                session.add(acceso)
                session.commit()
                if(result.estado == 1):
                    return result
                else:
                    return None
            else: 
            
                return None
        else:
            return None
    except Exception as e:
        print(e)


async def logOut(id_usuario):
    usuarioUpdated = session.query(Acceso).filter_by(id_usuario = id_usuario).order_by(desc(Acceso.id_acceso)).first()
    
    usuarioUpdated.fecha_hora_salida = func.now()
    session.commit()
    return True