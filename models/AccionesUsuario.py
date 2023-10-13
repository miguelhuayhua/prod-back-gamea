from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class AccionesUsuario(Base):
    __tablename__ = 'acciones_usuario'
    id_accion = Column(String, primary_key=True)
    fecha_hora_accion = Column(DateTime, default = func.now())
    tabla = Column(String)
    tipo = Column(String)
    id_usuario = Column(String)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_accion'))).scalar()
        return f"AU-{next_value}"
   