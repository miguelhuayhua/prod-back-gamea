from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, func, Sequence, select, ForeignKey
from sqlalchemy.orm import relationship
from database.conexion import engine

Base = declarative_base()


class Domicilio(Base):
    __tablename__ = 'domicilio'
    id_domicilio = Column(String, primary_key=True)
    distrito = Column(Integer)
    zona = Column(String)
    calle_av = Column(String)
    nro_vivienda = Column(Integer)
    area = Column(String)
    otra_area = Column(String)
    actual = Column(Integer, default=1)
    tipo_domicilio = Column(String)
    otro_domicilio = Column(String)
    ult_modificacion = Column(DateTime, default=func.now())
    estado = Column(Integer, default=1)

    id_adulto = Column(String)

    @classmethod
    def generate_id(cls):
        next_value = engine.execute(
            select(func.nextval('sec_id_domicilio'))).scalar()
        return f"VIV-{next_value}"
