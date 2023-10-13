# base de datos

from dateutil.parser import parse
from database.conexion import session
from models.Citado import Citado
from sqlalchemy import desc

async def insertCitado(data, id_citacion):
    try:
      for citado in data:
         if(citado.get('citado')==1):
            nombres_apellidos = citado.get('nombres_apellidos')
            citado = Citado(nombres_apellidos= nombres_apellidos, id_citado = Citado.generate_id(),
                              id_citacion = id_citacion)
            session.add(citado)
      session.commit()
      return True
    except Exception as e:
       print(e)
       return False
    


async def allCitadoByCaso(id_caso):
    citados= session.query(Citado).order_by(desc(Citado.id_citado)).filter_by(id_caso = id_caso).all()
    return citados


async def getCitadosByIdCitacion(id_citacion):
    citado = session.query(Citado).filter_by(id_citacion = id_citacion).all()
    return citado