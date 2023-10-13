from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func,  select
from database.conexion import engine
from sqlalchemy.orm import relationship
Base = declarative_base()


class AdultoMayor(Base):
    __tablename__ = 'adulto_mayor'
    id_adulto = Column(String, primary_key=True)
    nombre = Column(String)
    paterno = Column(String)
    materno = Column(String)
    edad = Column(Integer)
    ci = Column(Integer)
    genero = Column(String)
    f_nacimiento = Column(Date)
    estado_civil = Column(String)
    nro_referencia = Column(Integer)
    ocupacion = Column(String)
    beneficios = Column(String)
    grado = Column(String)
    expedido = Column(String)
    estado = Column(Integer, default=1)
    ult_modificacion = Column(DateTime, default=func.now())
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_adulto'))).scalar()
        return f"AM-{next_value}"
