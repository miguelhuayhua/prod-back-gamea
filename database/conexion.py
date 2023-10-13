from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
# conexion
engine = create_engine(os.getenv('DATABASE_URL'))
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# creación de la session
session = sessionLocal()
