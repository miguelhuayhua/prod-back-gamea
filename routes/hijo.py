
import tempfile

from fastapi.responses import FileResponse
from database.Hijo import listarHijos, getHijo, cambiarEstado, modificarHijo
from fastapi import APIRouter, Request
import pandas as pd
from database.conexion import session
routerHijo = APIRouter()
from database.AccionUsuario import setAccionUsuario

# creamos las diferentes rutas de manejo para cada caso





@routerHijo.post('/get')
async def obtenerHijo(request: Request):
    data = await request.json()
    id_hijo  = data.get('id_hijo')
    hijo = await getHijo(id_hijo=id_hijo)
    session.close()
    return hijo


@routerHijo.get('/all')
async def allHijos():
    hijos = await listarHijos()
    session.close()
    return hijos

@routerHijo.post('/estado')
async def changeEstado(request:Request):
    try:
        data = await request.json()
        id_hijo = data.get('id_hijo')
        await cambiarEstado(id_hijo=id_hijo)
        id_usuario = data.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'hijo','STATUS')
        session.close()
        return {"status":1}
    except Exception as e:
        session.close()
        print(e)
        return {"status":0}
    


@routerHijo.post('/update')
async def updateHijo(request:Request):
    try:
        hijo = await request.json()
        await modificarHijo(hijo = hijo)
        id_usuario = hijo.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'usuario','UPDATE')
        session.close()
        return {"status":1}
    except Exception as e:
        session.close()
        print(e)
        return {"status":0}
    

@routerHijo.get('/report')
async def reportHijo():
    dataHijo = await listarHijos()
    hijo = []
    for value in dataHijo:
        dict = value.__dict__
        dict.pop('_sa_instance_state')
        hijo.append(dict)
    dataframeHijo = pd.DataFrame.from_records(hijo)
    dataframeHijo['ult_modificacion'] = dataframeHijo['ult_modificacion'].dt.strftime('%Y-%m-%d %H:%M:%S')    
    
      # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Guarda el DataFrame en el archivo temporal en formato Excel
        dataframeHijo.to_excel(temp_file.name, sheet_name='hijos', index=False, engine='xlsxwriter')
    session.close()
    # Envía el archivo como respuesta utilizando FileResponse
    return FileResponse(temp_file.name, filename='archivo.xlsx')
