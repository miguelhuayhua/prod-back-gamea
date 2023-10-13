from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class Citacion(Base):
    __tablename__ = 'citacion'
    id_citacion = Column(String, primary_key=True)
    fecha_creacion = Column(String)
    id_caso = Column(String)
    fecha_citacion = Column(String)
    numero = Column(Integer)
    hora_citacion = Column(String)
    suspendido = Column(Integer)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_citacion'))).scalar()
        return f"C-{next_value}"
