# base de datos

from dateutil.parser import parse
from database.conexion import session
from models.Audiencia import Audiencia
from sqlalchemy import desc

async def insertAudiencia(data, id_citacion):
    try:
      causa = data.get('causa')
      observacion = data.get('observacion')
      audiencia = Audiencia(id_audiencia_suspendida = Audiencia.generate_id(),
                            causa= causa, 
                            observacion = observacion,
                            id_citacion = id_citacion)
      session.add(audiencia)
      session.commit()
      return True
    except Exception as e:
       print(e)
       return False
    
