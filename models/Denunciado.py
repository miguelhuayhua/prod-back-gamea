from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from database.conexion import engine

Base = declarative_base()


class Denunciado(Base):
    __tablename__ = 'denunciado'
    id_denunciado = Column(String, primary_key=True)
    nombres = Column(String)
    paterno = Column(String)
    materno = Column(String)
    genero = Column(String)
    parentezco = Column(String)
    ci = Column(Integer)
    expedido = Column(String)
    estado = Column(Integer, default=1)
    ult_modificacion = Column(DateTime, default=func.now())
    id_caso = Column(String)

    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_denunciado'))).scalar()
        return f"D-{next_value}"
