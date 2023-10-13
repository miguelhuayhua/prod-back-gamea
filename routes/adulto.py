import tempfile

from fastapi.responses import FileResponse
from database.AdultoMayor import listarAdulto, getAdulto, cambiarEstado, modificarAdulto
from database.Hijo import getHijosByIdAdulto
from fastapi import APIRouter, Request
import pandas as pd

from database.AccionUsuario import setAccionUsuario
from database.conexion import session
routerAdulto = APIRouter()


# creamos las diferentes rutas de manejo para cada caso


@routerAdulto.get('/npmunicos')
async def all():
    data = await listarAdulto()
    dictAdulto = []
    for adulto in data:
        dict = adulto.__dict__
        dict.pop('_sa_instance_state')
        dictAdulto.append(dict)
    dataframe = pd.DataFrame.from_records(dictAdulto)
    if (len(data) != 0):
        nombres = dataframe['nombre'].unique()
        paterno = dataframe['paterno']
        materno = dataframe['materno']
        nombres = nombres[nombres!='']
        apellidos = pd.concat([paterno, materno], axis=0).unique()
        apellidos = apellidos[apellidos !='']
        session.close()
        return {'nombres': nombres.tolist(), 'apellidos': apellidos.tolist()}
    else:
        session.close()
        return {'nombres': [], 'apellidos':[]}


@routerAdulto.post('/get')
async def obtenerAdulto(request: Request):
    data = await request.json()
    id_adulto  = data.get('id_adulto')
    adulto = await getAdulto(id_adulto=id_adulto)
    hijos = await getHijosByIdAdulto(adulto.id_adulto)
    session.close()
    return {"adulto":adulto, "hijos":hijos}


@routerAdulto.get('/all')
async def allAdultos():
    adultos = await listarAdulto()
    session.close()
    return adultos

@routerAdulto.post('/estado')
async def changeEstado(request:Request):
    try:
        data = await request.json()
        id_adulto = data.get('id_adulto')
        await cambiarEstado(id_adulto)
        id_usuario = data.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'adulto','STATUS')
        session.close()
        return {"status":1}
    except:
        session.close()
        return {"status":0}
    


@routerAdulto.post('/update')
async def updateAdulto(request:Request):
    try:
        adulto = await request.json()
        await modificarAdulto(adulto=adulto)
        id_usuario = adulto.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'adulto','UPDATE')
        session.close()
        return {"status":1}
    except:
        session.close()
        return {"status":0}
    

@routerAdulto.get('/report')
async def reportAdulto():
    dataAdulto = await listarAdulto()
    personal = []
    for adulto in dataAdulto:
        dict = adulto.__dict__
        dict.pop('_sa_instance_state')
        personal.append(dict)
    dataframeAdulto = pd.DataFrame.from_records(personal)
    dataframeAdulto['ult_modificacion'] = dataframeAdulto['ult_modificacion'].dt.strftime('%Y-%m-%d %H:%M:%S')    
    
      # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Guarda el DataFrame en el archivo temporal en formato Excel
        dataframeAdulto.to_excel(temp_file.name, sheet_name='adultos', index=False, engine='xlsxwriter')
    session.close()
    # Envía el archivo como respuesta utilizando FileResponse
    return FileResponse(temp_file.name, filename='archivo.xlsx')
