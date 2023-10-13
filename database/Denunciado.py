# base de datos

import genderize
from sqlalchemy import desc
from database.conexion import session, engine
from models.Denunciado import Denunciado


async def insertDenunciado(data, id_caso):
    materno = data.get('materno').strip().capitalize()
    paterno = data.get('paterno').strip().capitalize()
    nombres = data.get('nombres').strip().capitalize()
    genero = ''
    if(genderize.Genderize().get([nombres],country_id='ES', language_id='es')[0].get('gender')== 'female'):
        genero = 'Femenino'
    else:
        genero = 'Masculino'

    parentezco = data.get('parentezco')
    denunciado = Denunciado(id_denunciado=Denunciado.generate_id(), paterno=paterno,
                            materno=materno,
                            nombres=nombres,
                            parentezco=parentezco,
                            genero=genero,
                            id_caso=id_caso)

    session.add(denunciado)
    session.commit()
    return denunciado.id_denunciado



async def listarDenunciados():
    return session.query(Denunciado).order_by(desc(Denunciado.id_denunciado)).all()



async def getDenunciado(id_denunciado)->Denunciado:
    denunciado = session.query(Denunciado).filter_by(id_denunciado = id_denunciado).first()
    return denunciado


async def cambiarEstado(id_denunciado):
    denunciado = session.query(Denunciado).filter_by(id_denunciado = id_denunciado).first()
    if denunciado.estado ==0:
        denunciado.estado = 1
    else :
        denunciado.estado = 0
    session.commit()
    return True

async def modificarDenunciado(denunciado):
    nombres = denunciado.get('nombres')
    paterno = denunciado.get('paterno')
    materno = denunciado.get('materno')
    genero = denunciado.get('genero')
    ci = denunciado.get('ci')
    expedido = denunciado.get('expedido')
    denunciadoUpdated = session.query(Denunciado).filter_by(id_denunciado=denunciado.get('id_denunciado')).first()
    denunciadoUpdated.nombres = nombres
    denunciadoUpdated.paterno = paterno
    denunciadoUpdated.materno = materno
    denunciadoUpdated.ci = ci
    denunciadoUpdated.expedido= expedido
    denunciadoUpdated.genero = genero
    session.commit()
    return denunciadoUpdated.id_denunciado

async def getDenunciadoByCaso(id_caso)->Denunciado:
    denunciado = session.query(Denunciado).filter_by(id_caso = id_caso).first()
    return denunciado

