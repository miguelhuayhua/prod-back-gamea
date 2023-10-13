
from database.conexion import session
from models.Domicilio import Domicilio
from sqlalchemy import and_
async def insertarDomicilio(data, id_adulto):
    domicilios = session.query(Domicilio).filter_by(id_adulto = id_adulto).all()
    for d in domicilios:
        d.actual = 0
    distrito = data.get('distrito')
    zona = data.get('zona')
    calle_av = data.get('calle_av')
    nro_vivienda = data.get('nro_vivienda')
    area = data.get('area')
    tipo_domicilio = data.get('tipo_domicilio')
    otro_domicilio = data.get('otro_domicilio')
    otra_area = data.get('otra_area')
    domicilio = Domicilio(id_domicilio=Domicilio.generate_id(),
                          distrito=distrito,
                          zona=zona,
                          calle_av=calle_av,
                          nro_vivienda=nro_vivienda,
                          area=area,
                          otra_area=otra_area,
                          id_adulto=id_adulto,
                          otro_domicilio=otro_domicilio,
                          tipo_domicilio=tipo_domicilio)
    session.add(domicilio)
    session.commit()
    return domicilio.id_domicilio


async def listarDomicilio():
    return session.query(Domicilio).all()

async def getDomicilio(id_adulto)->Domicilio:
    domicilio = session.query(Domicilio).filter(and_(Domicilio.id_adulto == id_adulto,Domicilio.actual == 1,Domicilio.estado ==1)).first()
    return domicilio


async def modificarDomicilio(domicilio):
    domicilios = session.query(Domicilio).filter_by(id_adulto = domicilio.get('id_adulto')).all()
    for d in domicilios:
        d.actual = 0
    id_domicilio = domicilio.get('id_domicilio')
    distrito = domicilio.get('distrito')
    zona = domicilio.get('zona')
    calle_av = domicilio.get('calle_av')
    area = domicilio.get('area')
    otra_area = domicilio.get('otra_area')
    actual = domicilio.get('actual')
    nro_vivienda = domicilio.get('nro_vivienda')
    tipo_domicilio = domicilio.get('tipo_domicilio')
    otro_domicilio = domicilio.get('otro_domicilio')
    domicilioUpdated = session.query(Domicilio).filter_by(id_domicilio = id_domicilio).first()
    domicilioUpdated.distrito = distrito
    domicilioUpdated.nro_vivienda = nro_vivienda
    domicilioUpdated.zona = zona
    domicilioUpdated.calle_av = calle_av
    domicilioUpdated.area = area
    domicilioUpdated.otra_area = otra_area
    domicilioUpdated.actual = actual
    domicilioUpdated.tipo_domicilio = tipo_domicilio
    domicilioUpdated.otro_domicilio  =otro_domicilio
    session.commit()
    return domicilioUpdated.id_domicilio
 
async def obtenerDomicilioByIdAdulto(id_adulto):
    domicilios = session.query(Domicilio).filter_by(id_adulto = id_adulto).all()
    return domicilios
