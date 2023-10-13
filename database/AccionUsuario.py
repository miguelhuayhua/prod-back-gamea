# base de datos

from dateutil.parser import parse
from database.conexion import session
from models.Caso import Caso
from sqlalchemy import desc
from models.AccionesUsuario import AccionesUsuario


async def setAccionUsuario(id_usuario, tabla, tipo):
    accion = AccionesUsuario(id_accion = AccionesUsuario.generate_id(), id_usuario = id_usuario,
                             tabla = tabla, tipo = tipo)
    session.add(accion)
    session.commit()
    return accion.id_accion
