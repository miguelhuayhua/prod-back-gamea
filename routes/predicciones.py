import genderize
from fastapi import APIRouter, Request
import pandas as pd
from database.conexion import session
routerPredicciones = APIRouter()

@routerPredicciones.post('/genderize/predict')
async def predictGenderize(request: Request):
   data = await request.json()
   genero = 1
   nombres_apellidos = data.get('nombres_apellidos')
   nombres = nombres_apellidos.split(" ")[0]
   if(genderize.Genderize().get([nombres],country_id='ES', language_id='es')[0].get('gender')== 'female'):
      genero = 1
   else:
      genero = 0
   return {"genero":genero}
    