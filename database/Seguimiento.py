# base de datos

from dateutil.parser import parse
from database.conexion import session
from models.Seguimiento import Seguimiento
from sqlalchemy import desc

async def insertSeguimiento(data, id_caso):
    fecha_seguimiento = data.get('fecha_seguimiento')
    detalle_seguimiento = data.get('detalle_seguimiento')
    hora_seguimiento = data.get('hora_seguimiento')
    size = len(await allSeguimientoByCaso(id_caso))
    if(size<4):
        seguimiento = Seguimiento(detalle_seguimiento = detalle_seguimiento, id_seguimiento = Seguimiento.generate_id(),
                              id_caso = id_caso, fecha_seguimiento = fecha_seguimiento, hora_seguimiento = hora_seguimiento)
        session.add(seguimiento)
        session.commit()
        return seguimiento.id_seguimiento
    else:
        return None


async def allSeguimientoByCaso(id_caso):
    seguimientos= session.query(Seguimiento).order_by(desc(Seguimiento.id_seguimiento)).filter_by(id_caso = id_caso).all()
    return seguimientos
