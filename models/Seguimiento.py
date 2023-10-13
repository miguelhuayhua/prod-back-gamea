from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class Seguimiento(Base):
    __tablename__ = 'seguimiento'
    id_seguimiento = Column(String, primary_key=True)
    detalle_seguimiento = Column(String)
    id_caso = Column(String)
    fecha_seguimiento = Column(String)
    hora_seguimiento = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_seguimiento'))).scalar()
        return f"SG-{next_value}"
