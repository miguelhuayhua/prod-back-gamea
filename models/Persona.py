from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class Persona(Base):
    __tablename__ = 'persona'
    id_persona = Column(String, primary_key=True)
    nombres = Column(String)
    paterno = Column(String)
    materno = Column(String)
    genero = Column(String)
    profesion = Column(String)
    ci = Column(Integer)
    expedido = Column(String)
    celular = Column(Integer)
    f_nacimiento = Column(Date)
    cargo = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_persona'))).scalar()
        return f"P-{next_value}"
