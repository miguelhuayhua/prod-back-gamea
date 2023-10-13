
import os
import tempfile

from fastapi.responses import FileResponse
from database.Usuario import insertUsuario, verifyUsuario, cambiarEstado, listarUsuarios, modificarUsuario,getUsuario, getByNameAndPassword, getAccionesById, getAccesosById, logOut
from fastapi import APIRouter, Request
import pandas as pd
from database.conexion import session
from models.Usuario import Usuario
from models.AccesoUsuario import Acceso
from database.AccionUsuario import setAccionUsuario
routerUsuario = APIRouter()


# creamos las diferentes rutas de manejo para cada usuario
@routerUsuario.post('/verify')
async def obtenerusuario(request: Request):
    data = await request.json()
    if await verifyUsuario(usuario = data):
        session.close()
        return {"status":0}
    else:
        session.close()
        return {"status":1}
    
@routerUsuario.get('/all')
async def allusuarios():
    usuarios = await listarUsuarios()
    usuarios_json = [usuario.__dict__ for usuario in usuarios]
    for usuario_json in usuarios_json:
        if 'password' in usuario_json:
            del usuario_json['password']
    session.close()
    return usuarios_json

@routerUsuario.post('/estado')
async def changeEstado(request:Request):
    try:
        data = await request.json()
        id_usuario = data.get('id_usuario')
        await cambiarEstado(id_usuario=id_usuario)
        id_usuario = data.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'usuario','STATUS')
        session.close()
        return {"status":1}
    except:
        session.close()
        return {"status":0}
    


@routerUsuario.post('/update')
async def updateusuario(request:Request):
    try:
        usuario = await request.form()
        await modificarUsuario(usuario = usuario)
        id_usuario = usuario.get('id_usuario2')
        await setAccionUsuario(id_usuario,'usuario','UPDATE')
        session.close()
        return {"status":1}
    except Exception as e:
        session.close()
        print(e)
        return {"status":0}
    
@routerUsuario.post('/get')
async def obtenerUsuario(request: Request):
    data = await request.json()
    id_usuario  = data.get('id_usuario')
    usuario = await getUsuario(id_usuario= id_usuario)
    session.close()
    return usuario

@routerUsuario.post('/fotografia')
async def fotografiaUsuario(request: Request):
    data = await request.form()
    id_usuario = data.get('id_usuario')
    usuario = await getUsuario(id_usuario= id_usuario)
    file = data.get('fotografia')
    if(file != 'null'):
        file_path = os.path.join(file.filename)
        file_path = file_path.replace(' ','')
        file_path = file_path.lower()
        with open("public/usersimg/"+ file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        usuario.fotografia = f"/static/images/{file_path}"
    session.commit()
    session.close()
    return {"status":1}

@routerUsuario.post('/username')
async def usrName(request: Request):
    data = await request.json()
    id_usuario = data.get('id_usuario')
    username = data.get('usuario')
    usuario = await getUsuario(id_usuario= id_usuario)
    if(session.query(Usuario).filter_by(usuario = username).all()):
        session.close()
        return {"message":"Usuario en uso...","status":0}
    else:
        usuario.usuario = username
        session.commit()
        session.close()        
        return {"message":"Usuario modificado con éxito!, reinicie su sesión para ver cambios...","status":1}


@routerUsuario.post('/auth')
async def authUsuari(request: Request):
    data = await request.json()
    usuario = await getByNameAndPassword(data)
    if(usuario):
        session.query(Acceso).filter_by(id_usuario = usuario.id_usuario)
        session.close()
        return usuario
    else:
        session.close()
        return None

@routerUsuario.post('/out')
async def authUsuario(request: Request):
    data = await request.json()
    id_usuario = data.get('id_usuario')
    if(await logOut(id_usuario=id_usuario)):
        session.close()
        return {"status":1}
    else:
        session.close()
        return None


@routerUsuario.post('/insert')
async def insertarUsuario(request:Request):
    try:
        usuario = await request.form()
        await insertUsuario(data=  usuario)
        id_usuario = usuario.get('id_usuario')
        await setAccionUsuario(id_usuario,'usuario','INSERT')
        session.close()
        return {"status":1}
    except Exception as e:
        print(e)
        session.close()
        return {"status":0}

@routerUsuario.post('/getAccionesById')
async def getAccionesByIdF(request:Request):
    try:
        usuario = await request.json()
        acciones = await getAccionesById(usuario.get('id_usuario'))
        session.close()
        return acciones
    except Exception as e:
        print(e)
        session.close()
        return {"status":0}

@routerUsuario.post('/getAccesosById')
async def getAccesosByIdF(request:Request):
    try:
        usuario = await request.json()
        accesos = await getAccesosById(usuario.get('id_usuario'))
        session.close()
        return accesos
    except Exception as e:
        print(e)
        session.close()
        return {"status":0}

           
@routerUsuario.get('/report')
async def reportUsuario():
    dataUsuarios = await listarUsuarios()
    usuarios = []
    for usuario in dataUsuarios:
        dict = usuario.__dict__
        dict.pop('_sa_instance_state')
        usuarios.append(dict)
    dataframeUsuarios = pd.DataFrame.from_records(usuarios)
    del dataframeUsuarios['password']
    dataframeUsuarios['ult_modificacion'] = dataframeUsuarios['ult_modificacion'].dt.strftime('%Y-%m-%d %H:%M:%S')    
    
      # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Guarda el DataFrame en el archivo temporal en formato Excel
        dataframeUsuarios.to_excel(temp_file.name, sheet_name='usuarios', index=False, engine='xlsxwriter')
    session.close()
    # Envía el archivo como respuesta utilizando FileResponse
    return FileResponse(temp_file.name, filename='archivo.xlsx')
