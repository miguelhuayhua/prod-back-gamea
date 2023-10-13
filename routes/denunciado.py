import tempfile

from fastapi.responses import FileResponse
import pandas as pd
from database.Denunciado import getDenunciadoByCaso, cambiarEstado, listarDenunciados, getDenunciado, modificarDenunciado

from fastapi import APIRouter, Request
from database.conexion import session
from database.AccionUsuario import setAccionUsuario
routerDenunciado = APIRouter()



@routerDenunciado.post('/get')
async def obtenerDenunciado(request:Request):
    try:
        data = await request.json()
        id_caso = data.get('id_caso')
        denunciado = await getDenunciadoByCaso(id_caso=id_caso)
        session.close()
        return denunciado
    except:
        return {"status":0}
    

@routerDenunciado.post('/getById')
async def obtenerDenunciadoById(request:Request):
    try:
        data = await request.json()
        id_denunciado = data.get('id_denunciado')
        denunciado = await getDenunciado(id_denunciado=id_denunciado)
        session.close()
        return denunciado
    except:
        return {"status":0}
    
    

@routerDenunciado.get('/all')
async def alldenunciados():
    denunciados = await listarDenunciados()
    session.close()
    return denunciados

@routerDenunciado.post('/estado')
async def changeEstado(request:Request):
    try:
        data = await request.json()
        id_denunciado = data.get('id_denunciado')
        id_usuario = data.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'denunciado','STATUS')
        await cambiarEstado(id_denunciado=id_denunciado)
        session.close()
        return {"status":1}
    except:
        return {"status":0}
    
@routerDenunciado.post('/update')
async def updateDenunciado(request:Request):
    try:
        denunciado = await request.json()
        await modificarDenunciado(denunciado=denunciado)
        id_usuario = denunciado.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'denunciado','UPDATE')
        session.close()
        return {"status":1, "message":"Denunciado modificado con éxito..."}
    except Exception as e:
        print(e)
        session.close()
        return {"status":0, "message":"Ha ocurrido un error en el servidor..."}

@routerDenunciado.get('/report')
async def reportDenunciado():
    dataDenunciado = await listarDenunciados()
    denunciado = []
    for value in dataDenunciado:
        dict = value.__dict__
        dict.pop('_sa_instance_state')
        denunciado.append(dict)
    dataframeDenunciado = pd.DataFrame.from_records(denunciado)
    dataframeDenunciado['ult_modificacion'] = dataframeDenunciado['ult_modificacion'].dt.strftime('%Y-%m-%d %H:%M:%S')    
    
      # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Guarda el DataFrame en el archivo temporal en formato Excel
        dataframeDenunciado.to_excel(temp_file.name, sheet_name='denunciados', index=False, engine='xlsxwriter')
    session.close()
    # Envía el archivo como respuesta utilizando FileResponse
    return FileResponse(temp_file.name, filename='archivo.xlsx')
