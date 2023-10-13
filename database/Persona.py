# base de datos
from sqlalchemy import desc
from database.conexion import session
from models.Persona import Persona


async def insertPersona(data):
    nombres = data.get('nombres').capitalize().strip()
    paterno = data.get('paterno').capitalize().strip()
    materno = data.get('materno').capitalize().strip()
    profesion = data.get('profesion').capitalize().strip()
    expedido = data.get('expedido')
    ci = data.get('ci')
    celular = data.get('celular')
    f_nacimiento = data.get('f_nacimiento')
    cargo = data.get('cargo')
    genero = data.get('genero')
    persona = Persona(nombres = nombres, paterno = paterno, materno = materno, ci = ci, celular = celular, 
                      profesion= profesion,
                      f_nacimiento = f_nacimiento, cargo = cargo , genero = genero, id_persona = Persona.generate_id(),
                      expedido = expedido)
    session.add(persona)
    session.commit()
    return persona.id_persona

async def getPersonasByIdAdulto(id_adulto):
    personas = session.query(Persona).filter_by(id_adulto=id_adulto).all()
    return personas


async def listarPersonas():
    return session.query(Persona).order_by(desc(Persona.id_persona)).all()



async def getPersona(id_persona)->Persona:
    persona = session.query(Persona).filter_by(id_persona = id_persona).first()
    return persona


async def cambiarEstado(id_persona):
    persona = session.query(Persona).filter_by(id_persona = id_persona).first()
    if persona.estado ==0:
        persona.estado = 1
    else :
        persona.estado= 0
    session.commit()
    return True

async def modificarPersona(persona):
    nombres = persona.get('nombres').capitalize().strip()
    paterno = persona.get('paterno').capitalize().strip()
    materno = persona.get('materno').capitalize().strip()
    profesion = persona.get('profesion').capitalize().strip()
    expedido = persona.get('expedido')
    ci = persona.get('ci')
    celular = persona.get('celular')
    f_nacimiento = persona.get('f_nacimiento')
    cargo = persona.get('cargo')
    genero = persona.get('genero')
    personaUpdated = session.query(Persona).filter_by(id_persona  = persona.get('id_persona')).first()
    personaUpdated.nombres = nombres,
    personaUpdated.paterno = paterno
    personaUpdated.materno = materno
    personaUpdated.ci = ci
    personaUpdated.expedido = expedido
    personaUpdated.profesion = profesion
    personaUpdated.celular = celular
    personaUpdated.f_nacimiento = f_nacimiento 
    personaUpdated.cargo = cargo
    personaUpdated.genero = genero
    session.commit()
    return personaUpdated.id_persona
 
