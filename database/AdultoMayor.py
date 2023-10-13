# base de datos

import datetime
from dateutil.parser import parse
from fastapi import Request
from database.conexion import session, engine
from models.AdultoMayor import AdultoMayor
from models.Hijo import Hijo
from sqlalchemy import desc


async def insertAdulto(data):
    print(data)
    ci = data.get('ci')
    edad = data.get('edad')
    grado = data.get('grado')
    estado_civil = data.get('estado_civil')
    f_nacimiento = parse(data.get('f_nacimiento')).date()
    materno = data.get('materno').strip().capitalize()
    paterno = data.get('paterno').strip().capitalize()
    nombre = data.get('nombre').strip().capitalize()
    nro_referencia = data.get('nro_referencia')
    genero = data.get('genero')
    expedido = data.get('expedido')
    beneficios = data.get('beneficios')
    ocupacion = data.get('ocupacion')
    adultoMayor = AdultoMayor(id_adulto=AdultoMayor.generate_id(), ci=ci, edad=edad, estado_civil=estado_civil, f_nacimiento=f_nacimiento,  paterno=paterno,
                              materno=materno, grado=grado,
                              nombre=nombre, nro_referencia=nro_referencia, genero=genero,  beneficios=beneficios,
                              ocupacion=ocupacion, expedido= expedido)

    session.add(adultoMayor)
    session.commit()
    return adultoMayor.id_adulto


async def listarAdulto():
    adultos = session.query(AdultoMayor).order_by(desc(AdultoMayor.id_adulto)).all()
    return adultos


async def getUltimoAdulto():
    return None

async def getAdulto(id_adulto)->AdultoMayor:
    adulto = session.query(AdultoMayor).filter_by(id_adulto = id_adulto).first()
    return adulto

async def cambiarEstado(id_adulto):
    adulto = session.query(AdultoMayor).filter_by(id_adulto = id_adulto).first()
    if adulto.estado ==0:
        adulto.estado = 1
    else :
        adulto.estado= 0
    session.commit()
    return True

async def modificarAdulto(adulto):
    ci = adulto.get('ci')
    edad = adulto.get('edad')
    grado = adulto.get('grado')
    estado_civil = adulto.get('estado_civil')
    f_nacimiento = parse(adulto.get('f_nacimiento')).date()
    materno = adulto.get('materno').strip().capitalize()
    paterno = adulto.get('paterno').strip().capitalize()
    nombre = adulto.get('nombre').strip().capitalize()
    nro_referencia = adulto.get('nro_referencia')
    genero = adulto.get('genero')
    beneficios = adulto.get('beneficios')
    ocupacion = adulto.get('ocupacion')
    adultoUpdated = session.query(AdultoMayor).filter_by(id_adulto=adulto.get('id_adulto')).first()
    adultoUpdated.nombre = nombre
    adultoUpdated.paterno = paterno
    adultoUpdated.ci = ci
    adultoUpdated.edad = edad
    adultoUpdated.grado = grado
    adultoUpdated.estado_civil = estado_civil
    adultoUpdated.f_nacimiento = f_nacimiento
    adultoUpdated.materno = materno
    adultoUpdated.nro_referencia = nro_referencia
    adultoUpdated.genero = genero
    adultoUpdated.beneficios = beneficios
    adultoUpdated.ocupacion = ocupacion
    adultoUpdated.ult_modificacion = datetime.datetime.now()
    session.commit()
    return adultoUpdated.id_adulto
 

