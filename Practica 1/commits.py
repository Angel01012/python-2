import psycopg2
from logger_base import log

conexion = psycopg2.connect(user="postgres", password="162460132", host="127.0.0.1",port="5432",
                            database="practica1")

try:
    conexion.autocommit=False
    cursor = conexion.cursor
    sentencia = "INSERT INTO cliente(Nombre) Values(%s)"
    nombre="Jose"
    valores = (nombre,)
    cursor.execute(sentencia,valores)
    log.debug("Insert")
    sentencia =  "UPDATE cliente SET Nombre=%s WHERE idCliente=%s"
    valores = ("Polar",2)
    cursor.execute(sentencia,valores)
    log.debug("Sentencia update")
    conexion.commit()
except Exception as e:
    conexion.rollback()
    log.error(e)