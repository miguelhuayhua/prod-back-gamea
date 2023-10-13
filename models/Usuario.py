from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(String, primary_key=True)
    usuario = Column(String)
    password = Column(String)
    fotografia = Column(String)
    id_persona = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)
    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_usuario'))).scalar()
        return f"U-{next_value}"
    def exclude_fields(self):
        return ['password']