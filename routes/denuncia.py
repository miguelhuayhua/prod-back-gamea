from database.AdultoMayor import insertAdulto
from database.Domicilio import insertarDomicilio
from database.Denunciado import insertDenunciado
from database.Hijo import insertHijo
from database.Caso import insertCaso
from fastapi import APIRouter, Request
from database.AccionUsuario import setAccionUsuario
from database.conexion import session
routerDenuncia = APIRouter()
# funciones de modelos de la base de datos

# creamos las diferentes rutas de manejo para cada caso


@routerDenuncia.post('/insert')
async def insertDenuncia(request: Request):
    try:
        
        data = await request.json()
        datosGenerales = data.get('datosGenerales')
        id_usuario = data.get('usuario').get('id_usuario')
        id_adulto = await insertAdulto(datosGenerales)
        await insertHijo(datosGenerales.get('hijos'), id_adulto)
        datosUbicacion = data.get('datosUbicacion')
        await insertarDomicilio(datosUbicacion, id_adulto)
        # datos a colocar en Caso
        descripcionHechos = data.get('descripcionHechos')
        descripcionPeticion = data.get('descripcionPeticion')
        accionRealizada = data.get('accionRealizada')
        datosDenuncia = data.get('datosDenuncia')
        datosDenuncia['peticion'] = descripcionPeticion
        datosDenuncia['descripcion_hechos'] = descripcionHechos
        datosDenuncia['accion_realizada'] = accionRealizada
        id_caso = await insertCaso(datosDenuncia, id_adulto)
        await setAccionUsuario(id_usuario, 'caso','CREATE')
        datosDenunciado = data.get('datosDenunciado')
        await insertDenunciado(datosDenunciado, id_caso)
        session.close()
        return {"response": "Los datos se han registrado correctamente...", "status": 1}
    except Exception as e:
        session.close()
        print(e)
        return {"response": "Ha ocurrido un error en el servidor...", "status": 0}
