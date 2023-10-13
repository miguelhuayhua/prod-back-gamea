import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# importamos todas las rutas que creamos en la carpeta "routes"
from routes.adulto import routerAdulto
from routes.denuncia import routerDenuncia
from routes.caso import routerCaso
from routes.denunciado import routerDenunciado
from routes.domicilio import routerDomicilio
from routes.usuario import routerUsuario
from routes.persona import routerPersona
from routes.hijo import routerHijo
from routes.predicciones import routerPredicciones
from routes.graficos import routerGraficos
app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8888",
    "http://localhost",
    "app://."
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# colocado de las rutas en la aplicación principal
app.include_router(routerAdulto, prefix='/adulto')
app.include_router(routerDenuncia, prefix='/denuncia')
app.include_router(routerCaso, prefix='/caso')
app.include_router(routerDenunciado, prefix='/denunciado')
app.include_router(routerDomicilio, prefix='/domicilio')
app.include_router(routerHijo, prefix='/hijo')
app.include_router(routerPersona , prefix='/persona')
app.include_router(routerUsuario , prefix='/usuario')
app.include_router(routerPredicciones, prefix='/ml')
app.include_router(routerGraficos, prefix="/charts")


app.mount("/public", StaticFiles(directory=os.path.join(os.getcwd(), "public")), name="public")
@app.get("/static/images/{image_name}")
def get_image_url(image_name:str):
    image_path = os.path.join(os.getcwd(), "public/usersimg", image_name)
    return FileResponse(image_path)
