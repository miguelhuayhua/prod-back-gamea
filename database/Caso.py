# base de datos

from dateutil.parser import parse
from database.conexion import session
from models.Caso import Caso
from sqlalchemy import desc
from models.ActaCompromiso import ActaCompromiso
from models.Denunciado import Denunciado
from sqlalchemy import and_
async def insertCaso(data, id_adulto):
    fecha_registro = data.get('fecha_registro')
    tipologia = data.get('tipologia')
    year = parse(fecha_registro).year
    hora_registro = data.get('hora_registro')
    nro_caso = str(data.get('nro_caso')) + "/"+str(year)
    descripcion_hechos = data.get('descripcion_hechos')
    peticion = data.get('peticion')
    accion_realizada = data.get('accion_realizada')
    if(session.query(Caso).filter_by(nro_caso = nro_caso).first()):
        ult_caso = await getUltimoCaso()
        ult_nro_caso = int(ult_caso.nro_caso.split("/")[0])+1
        nro_caso = str(ult_nro_caso) + "/"+str(year)
    caso = Caso(id_caso=Caso.generate_id(),
                fecha_registro=fecha_registro,
                hora_registro=hora_registro,
                tipologia=tipologia,
                nro_caso=nro_caso,
                descripcion_hechos=descripcion_hechos,
                peticion=peticion,
                accion_realizada=accion_realizada,
                id_adulto=id_adulto)
    session.add(caso)
    session.commit()
    return caso.id_caso


async def getUltimoCaso():
    return session.query(Caso).order_by(desc(Caso.id_caso)).first()

async def allCasos(estado:bool):
    if(estado):
        return session.query(Caso).order_by(desc(Caso.id_caso)).all()
    else:
        return session.query(Caso).filter_by(estado = 1).order_by(desc(Caso.id_caso)).all()

async def getByIdAdulto(id_adulto):
    return session.query(Caso).filter_by(id_adulto = id_adulto).order_by(desc(Caso.id_caso)).all()
   

async def cambiarEstado(id_caso):
    caso = session.query(Caso).filter_by(id_caso = id_caso).first()
    if caso.estado ==0:
        caso.estado = 1
    else :
        caso.estado= 0
    session.commit()
    return True


async def modificarCaso(caso):
    try:
        casoUpdated = session.query(Caso).filter_by(id_caso=caso.get('id_caso')).first()
        casoUpdated.descripcion_hechos = caso.get('descripcion_hechos')
        casoUpdated.peticion = caso.get('peticion')
        casoUpdated.accion_realizada = caso.get('accion_realizada')
        session.commit()
        return True
    except:
        return False


async def getCaso(id_caso)->Caso:
    caso = session.query(Caso).filter(and_(Caso.id_caso ==id_caso, Caso.estado == 1)).first()
    return caso


async def generaActaCompromiso(id_caso, compromisos, denunciado):
    caso = session.query(Caso).filter_by(id_caso = id_caso).first()
    caso.estado = 0
    for value in compromisos:
        c = ActaCompromiso(compromiso = value.get('compromiso'), id_caso = id_caso,
                           id_compromiso = ActaCompromiso.generate_id())
        session.add(c)
        session.commit()
    d = session.query(Denunciado).filter_by(id_denunciado = denunciado.get('id_denunciado')).first()
    d.ci = denunciado.get('ci')
    d.expedido = denunciado.get('expedido')
    session.commit()
    return True
