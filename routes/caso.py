from database.Caso import getUltimoCaso, allCasos, cambiarEstado, modificarCaso,getCaso, generaActaCompromiso, getByIdAdulto
from database.AdultoMayor import listarAdulto
from database.Seguimiento import insertSeguimiento, allSeguimientoByCaso
from database.Hijo import listarHijos
from database.Citacion import allCitacionByCaso, insertCitacion, suspenderCitacion
from database.Citado import insertCitado, getCitadosByIdCitacion
from database.Audiencia import insertAudiencia
from fastapi import APIRouter, Request

from database.conexion import session
from fastapi.responses import FileResponse
import tempfile

import pandas as pd
from database.AccionUsuario import setAccionUsuario

routerCaso = APIRouter()


# creamos las diferentes rutas de manejo para cada caso
@routerCaso.get('/all')
async def allCaso():
    casos =  await allCasos(estado = True)
    session.close()
    return casos

@routerCaso.get('/all_by_estado')
async def allCaso():
    casos =  await allCasos(estado = False)
    session.close()
    return casos

@routerCaso.post('/get')
async def obtenercaso(request: Request):
    data = await request.json()
    id_caso  = data.get('id_caso')
    caso = await getCaso(id_caso=id_caso)
    session.close()
    return caso

@routerCaso.post('/getByIdAdulto')
async def obtenerCasoPorIdAdulto(request: Request):
    data = await request.json()
    id_adulto  = data.get('id_adulto')
    caso = await getByIdAdulto(id_adulto = id_adulto)
    session.close()
    return caso


@routerCaso.get('/getultimo')
async def lastCaso():
    caso = await getUltimoCaso()
    session.close()
    return caso

@routerCaso.post('/estado')
async def changeEstado(request:Request):
    try:
        data = await request.json()
        id_usuario = data.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'caso','STATUS')
        id_caso = data.get('id_caso')
        await cambiarEstado(id_caso)
        session.close()
        return {"status":1}
    except:
        session.close()
        return {"status":0}
    

@routerCaso.post('/update')
async def updateCaso(request:Request):
    try:
        caso = await request.json()
        await modificarCaso(caso)
        id_usuario = caso.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'caso','UPDATE')
        session.close()
        return {"status":1}
    except:
        session.close()
        return {"status":0}
    
@routerCaso.get('/report')
async def reportCaso():
    dataCasos = await allCasos(estado=True)
    casos = []
    for caso in dataCasos:
        dict = caso.__dict__
        dict.pop('_sa_instance_state')
        casos.append(dict)
    dataframeCasos = pd.DataFrame.from_records(casos)
    dataHijos = await listarHijos()
    hijos = []
    for hijo in dataHijos:
        dict = hijo.__dict__
        dict.pop('_sa_instance_state')
        hijos.append(dict)
    dataAdultos = await listarAdulto()
    adultos = []
    for adulto in dataAdultos:
        dict = adulto.__dict__
        dict.pop('_sa_instance_state')
        adultos.append(dict)
    dataframeAdultos = pd.DataFrame.from_records(adultos)
    unido1 = pd.merge(dataframeAdultos, dataframeCasos, on="id_adulto", how="inner")
    unido1['nro_referencia'] = unido1['nro_referencia'].astype(str)
    unido1['ult_modificacion_y'] = unido1['ult_modificacion_y'].dt.strftime('%Y-%m-%d %H:%M:%S')    
    unido1['ult_modificacion_x'] = unido1['ult_modificacion_x'].dt.strftime('%Y-%m-%d %H:%M:%S')    
    unido1['f_nacimiento'] = pd.to_datetime(unido1['f_nacimiento'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    unido1.reindex(['nombre, paterno, materno'])
      # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Guarda el DataFrame en el archivo temporal en formato Excel
        unido1.to_excel(temp_file.name, sheet_name='hoja1', index=False, engine='xlsxwriter')
    session.close()
    # Envía el archivo como respuesta utilizando FileResponse
    return FileResponse(temp_file.name, filename='archivo.xlsx')



#SEGUIMIENTOS
@routerCaso.post('/seguimiento/add')
async def addCaso(request:Request):
    try:
        seguimiento = await request.json()
        await insertSeguimiento(seguimiento, seguimiento.get('id_caso'))
        id_usuario = seguimiento.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario,'seguimiento','INSERT')
        session.close()
        return {"status":1}
    except:
        session.close()
        return {"status":0}
    
@routerCaso.post('/seguimiento/all')
async def allCaso(request:Request):
    data= await request.json()
    id_caso = data.get('id_caso')
    seguimientos = await allSeguimientoByCaso(id_caso)
    session.close()
    return seguimientos


#CITACIONES
@routerCaso.post('/citacion/all')
async def allCitacion(request:Request):
    data = await request.json()
    id_caso = data.get('id_caso')
    citaciones = await allCitacionByCaso(id_caso)
    session.close()
    return citaciones

@routerCaso.post('/citados/get')
async def getCitados(request:Request):
    data = await request.json()
    citados = await getCitadosByIdCitacion(data.get('id_citacion'))
    session.close()
    return citados


@routerCaso.post('/citacion/add')
async def addCitacion(request:Request):
    try:
        
        citacion = await request.json()
        id_usuario = citacion.get('usuario').get('id_usuario')
        id_citacion = await insertCitacion(citacion.get('citacion'), citacion.get('id_caso'), citacion.get('numero'))
        res = await insertCitado(citacion.get('citados'), id_citacion= id_citacion)
        await setAccionUsuario(id_usuario, 'citacion', 'INSERT')
        if (res):
            session.close()
            return {"status":1}
        else:
            session.close()
            return {"status":0, "message":"No se puede generar mas citaciones..."}
    except Exception as e:
        session.close()
        return {"status":0, "message":"Ha ocurido un error en el servidor..."}


#AUDIENCIAS SUSPENDIDAS

@routerCaso.post('/audiencia/add')
async def addCitacion(request:Request):
    try:
        data = await request.json()
        id_citacion = data.get('id_citacion')
        id_usuario = data.get('usuario').get('id_usuario')
        await setAccionUsuario(id_usuario, 'detalle_audiencia_suspendida','INSERT')
        if(await insertAudiencia(data.get('audiencia'), id_citacion=id_citacion)):
            await suspenderCitacion(id_citacion)
            session.close()
            return {"status":1,"message": "Audiencia suspendida correctamente"}

        else:
            session.close()
            return {"status":0,"message": "No se pudo suspender la audiencia debido a un error..."}
    except Exception as e:
        print(e)
        session.close()
        return {"status":0, "message":"Ha ocurido un error en el servidor..."}

#ACTA COMPROMISO
@routerCaso.post("/acta-compromiso")
async def generarActaCompromiso(request:Request):
    try:
        data = await request.json()
        id_usuario = data.get('usuario').get('id_usuario')
        if(await generaActaCompromiso(data.get('id_caso'), data.get('compromisos'),data.get('denunciado')) ):
            await setAccionUsuario(id_usuario, 'detalle_acta_compromiso', 'INSERT')
            session.close()
            return {"status":1}
        else:
            session.close()
            return {"status":0, "message":"No se pudo insertar los datos..."}
    except Exception as e:
        print(e)
        session.close()
        return {"status":0, "message":"Ha ocurido un error en el servidor..."}

