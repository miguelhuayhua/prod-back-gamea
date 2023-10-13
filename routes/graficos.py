from fastapi import APIRouter, Request
import pandas as pd
from database.conexion import session

from sqlalchemy import text
routerGraficos= APIRouter()


# creamos las diferentes rutas de manejo para cada caso


@routerGraficos.get('/dashboard')
async def chartDashboard(request: Request):
    data1 = session.execute("SELECT * FROM caso_x_distrito()").fetchall()
    print('1')
    data2 = session.execute("SELECT * FROM acciones_x_casos()").fetchall()
    print('2')
    data3 = session.execute("SELECT * FROM casos_x_mes()").fetchall()
    data4 = session.execute("SELECT * FROM conteo_tipologia()").fetchall()
    data5 = session.execute("SELECT * FROM genero_x_casos()").fetchall()
    data6 = session.execute("SELECT * FROM rango_edades()").fetchall()
    rango_edades = {"rango_edades":[value[0] for value in data6], "cantidad":[value[1] for value in data6]}
    casos_x_mes_actual = session.execute("SELECT * FROM casos_x_mes_actual()").fetchall()[0]['cantidad']
    casos_x_dia = session.execute("SELECT * FROM casos_x_dia()").fetchall()[0]['cantidad']
    citaciones_x_mes = session.execute("SELECT * FROM citaciones_x_mes()").fetchall()[0]['cantidad']
    caso_x_distrito = {"distrito":[value[0] for value in data1], "cantidad":[value[1] for value in data1]}
    proximas_citaciones = session.execute("SELECT * FROM proximas_citaciones()").fetchall()
    acciones_x_casos = {"accion":[value[0] for value in data2], "cantidad":[value[1] for value in data2]}
    casos_x_mes = {"mes":[value[0] for value in data3], "cantidad":[value[1] for value in data3]}
    genero_x_casos = {"genero":[value[0] for value in data5], "cantidad":[value[1] for value in data5]}
    suspendidos_x_mes = session.execute("SELECT * FROM suspendidos_x_mes()").fetchall()[0]['cantidad']
    conteo_tipologia = {"tipologia":[value[0] for value in data4], "cantidad":[value[1] for value in data4]}
    session.close()
    return {"caso_x_distrito":caso_x_distrito, "acciones_x_casos":acciones_x_casos, "casos_x_mes":casos_x_mes, "conteo_tipologia":conteo_tipologia,
            "casos_x_genero":genero_x_casos, "suspendidos_x_mes":suspendidos_x_mes, "casos_x_dia": casos_x_dia, "casos_x_mes_actual":casos_x_mes_actual,
            "citaciones_x_mes":citaciones_x_mes, "proximas_citaciones":proximas_citaciones,
            "rango_edades":rango_edades}