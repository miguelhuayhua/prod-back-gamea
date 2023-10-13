from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from database.conexion import engine

Base = declarative_base()


class Caso(Base):
    __tablename__ = 'caso'
    id_caso = Column(String, primary_key=True)
    fecha_registro = Column(String)
    hora_registro = Column(String)
    tipologia = Column(String)
    nro_caso = Column(String)
    descripcion_hechos = Column(String)
    peticion = Column(String)
    accion_realizada = Column(String)
    id_adulto = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    id_adulto = Column(String)

    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_caso'))).scalar()
        return f"C-{next_value}"
