from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from database.conexion import engine

Base = declarative_base()


class Audiencia(Base):
    __tablename__ = 'detalle_audiencia_suspendida'
    id_audiencia_suspendida = Column(String, primary_key=True)
    causa = Column(String)
    observacion = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    id_citacion= Column(String)

    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_audiencia_suspendida'))).scalar()
        return f"AU-{next_value}"
