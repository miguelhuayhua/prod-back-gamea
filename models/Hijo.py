from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class Hijo(Base):
    __tablename__ = 'hijo'
    id_hijo = Column(String, primary_key=True)
    nombres_apellidos = Column(String)
    genero = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    id_adulto = Column(String)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_hijo'))).scalar()
        return f"H-{next_value}"
