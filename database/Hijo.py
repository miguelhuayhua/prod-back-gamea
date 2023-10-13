# base de datos

from dateutil.parser import parse
from sqlalchemy import desc
from database.conexion import session
from models.Hijo import Hijo

import genderize

async def insertHijo(hijos, id_adulto):
    for nombre_apellidos in hijos:
        genero = ''
        nombre = nombre_apellidos.split(' ')[0]
        if(genderize.Genderize().get([nombre],country_id='ES', language_id='es')[0].get('gender')== 'female'):
            genero = 'Femenino'
        else:
            genero = 'Masculino'
        hijo = Hijo(id_hijo=Hijo.generate_id(),
                    nombres_apellidos=nombre_apellidos.strip(),
                    id_adulto=id_adulto,
                    genero = genero
                    )
        session.add(hijo)
    session.commit()
    return len(hijos)

async def getHijosByIdAdulto(id_adulto):
    hijos = session.query(Hijo).filter_by(id_adulto=id_adulto).all()
    return hijos


async def listarHijos():
    return session.query(Hijo).order_by(desc(Hijo.id_hijo)).all()



async def getHijo(id_hijo)->Hijo:
    hijo = session.query(Hijo).filter_by(id_hijo = id_hijo).first()
    return hijo


async def cambiarEstado(id_hijo):
    hijo = session.query(Hijo).filter_by(id_hijo = id_hijo).first()
    if hijo.estado ==0:
        hijo.estado = 1
    else :
        hijo.estado= 0
    session.commit()
    return True

async def modificarHijo(hijo):
    nombres_apellidos = hijo.get('nombres_apellidos')
    genero = hijo.get('genero')
    hijoUpdated = session.query(Hijo).filter_by(id_hijo=hijo.get('id_hijo')).first()
    hijoUpdated.nombres_apellidos = nombres_apellidos
    hijoUpdated.genero = genero
    session.commit()
    return hijoUpdated.id_hijo
 
