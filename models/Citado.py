from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class Citado(Base):
    __tablename__ = 'citado'
    id_citado = Column(String, primary_key=True)
    id_citacion = Column(String)
    nombres_apellidos = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_citado'))).scalar()
        return f"CI-{next_value}"
