from Alumno import Alumno 
from cursorDelPool import CursorDelPool
from Conexion import Conexion
from logger_base import log

class AlumnoDAO:
    _SELECCIONAR = "SELECT * FROM alumno ORDER BY num_control"
    _INSERTAR = "INSERT INTO alumno (num_control,nombre,apellido,edad) VALUES (%s,%s,%s,%s)"
    _ACTUALIZAR = "UPDATE alumno SET nombre=%s,apellido=%s,edad=%s WHERE num_control=%s"
    _ELIMINAR = "DELETE FROM alumno WHERE num_control=%s"

    @classmethod
    def seleccionar(cls):
        with CursorDelPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            alumnos = []
            for r in registros:
                alumno = Alumno(r[0],r[1],r[2],r[3])
                alumnos.append(alumno)
            return alumnos
    @classmethod
    def insertar(cls,alumno):
        with CursorDelPool() as cursor:
            valores = (alumno.NumControl,alumno.Nombre, alumno.Apellido, alumno.Edad)
            cursor.execute(cls._INSERTAR,valores)
            return cursor.rowcount
    @classmethod
    def actualizar(cls,alumno):
        with CursorDelPool() as cursor:
            valores = (alumno.Nombre, alumno.Apellido, alumno.Edad, alumno.NumControl)
            cursor.execute(cls._ACTUALIZAR,valores)
            return cursor.rowcount
    @classmethod
    def eliminar(cls,alumno):
        with CursorDelPool() as cursor:
            valores = (alumno.NumControl,)
            cursor.execute(cls._ELIMINAR,valores)
            return cursor.rowcount
        
if __name__ == "__main__":
    # # #insertar
    # alumno1 = Alumno(num_control=2,nombre="eduardo",apellido="leyva",edad=21)
    # alumnosInsertados = AlumnoDAO.insertar(alumno1)
    # log.debug(f"Alumno Agregados {alumnosInsertados}")

    # # #actualizar
    # alumno = Alumno(nombre="jose",apellido="martinez",edad=22,num_control=2)
    # alumnosActualizados = AlumnoDAO.actualizar(alumno)
    # log.debug(f"alumno Actualizados {alumnosActualizados}")

    # # #eliminar
    # alumno = Alumno(num_control=2)
    # alumnosEliminados = AlumnoDAO.eliminar(alumno)
    # log.debug(f"Alumno Eliminados {alumnosEliminados}")

    #Leer
    alumno = AlumnoDAO.seleccionar()
    for a in alumno:
        log.debug(a)