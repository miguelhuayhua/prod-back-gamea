
import tempfile

from fastapi.responses import FileResponse
from database.Persona import cambiarEstado, insertPersona, listarPersonas , getPersona, modificarPersona
from fastapi import APIRouter, Request
import pandas as pd
from database.conexion import session
from database.AccionUsuario import setAccionUsuario
routerPersona = APIRouter()


# creamos las diferentes rutas de manejo para cada caso





@routerPersona.post('/get')
async def obtenerpersona(request: Request):
    data = await request.json()
    id_persona  = data.get('id_persona')
    persona = await getPersona(id_persona=id_persona)
    return persona


@routerPersona.get('/all')
async def allpersonas():
    personas = await listarPersonas()
    session.close()
    return personas

@routerPersona.post('/estado')
async def changeEstado(request:Request):
    try:
        data = await request.json()
        id_persona = data.get('id_persona')
        await cambiarEstado(id_persona=id_persona)
        id_usuario = data.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'persona','STATUS')
        session.close()
        return {"status":1}
    except:
        session.close()
        return {"status":0}
    


@routerPersona.post('/update')
async def updatepersona(request:Request):
    try:
        persona = await request.json()
        await modificarPersona(persona = persona)
        id_usuario = persona.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'persona','UPDATE')
        session.close()
        return {"status":1}
    except Exception as e:
        session.close()
        print(e)
        return {"status":0}
    


@routerPersona.post('/insert')
async def insertarPersona(request:Request):
    try:
        persona = await request.json()
        id_persona = await insertPersona(data=  persona)
        id_usuario = persona.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'persona','INSERT')
        session.close()
        return {"status":1, 'id_persona' : id_persona}
    except Exception as e:
        session.close()
        print(e)
        return {"status":0}
    
       
@routerPersona.get('/report')
async def reportPersona():
    dataPersona = await listarPersonas()
    personal = []
    for usuario in dataPersona:
        dict = usuario.__dict__
        dict.pop('_sa_instance_state')
        personal.append(dict)
    dataframePersona = pd.DataFrame.from_records(personal)
    dataframePersona['ult_modificacion'] = dataframePersona['ult_modificacion'].dt.strftime('%Y-%m-%d %H:%M:%S')    
    
      # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Guarda el DataFrame en el archivo temporal en formato Excel
        dataframePersona.to_excel(temp_file.name, sheet_name='usuarios', index=False, engine='xlsxwriter')
    session.close()
    # Envía el archivo como respuesta utilizando FileResponse
    return FileResponse(temp_file.name, filename='archivo.xlsx')
