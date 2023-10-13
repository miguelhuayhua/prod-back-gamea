from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, select
from database.conexion import engine

Base = declarative_base()


class Acceso(Base):
    __tablename__ = 'acceso_usuario'
    id_acceso = Column(String, primary_key=True)
    fecha_hora_acceso= Column(DateTime, default=func.now())
    fecha_hora_salida= Column(DateTime)
    estado = Column(Integer, default = 1)
    id_usuario = Column(String)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_acceso'))).scalar()
        return f"ACU-{next_value}"
   