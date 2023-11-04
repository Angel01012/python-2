from Proveedores import Proveedor 
from cursorDelPool import CursorDelPool
from Conexion import Conexion
from logger_base import log

class ProveedorDAO:
    _SELECCIONAR = "SELECT * FROM proveedor ORDER BY id"
    _INSERTAR = "INSERT INTO proveedor (id,nombre,rfc,direccion, telefono) VALUES (%s,%s,%s,%s,%s)"
    _ACTUALIZAR = "UPDATE proveedor SET nombre=%s,rfc=%s,direccion=%s,telefono=%s WHERE id=%s"
    _ELIMINAR = "DELETE FROM proveedor WHERE id=%s"

    @classmethod
    def seleccionar(cls):
        with CursorDelPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            proveedores = []
            for r in registros:
                proveedor = Proveedor(r[0],r[1],r[2],r[3],r[4])
                proveedores.append(proveedor)
            return proveedores
    @classmethod
    def insertar(cls,proveedor):
        with CursorDelPool() as cursor:
            valores = (proveedor.Id,proveedor.Nombre, proveedor.RFC, proveedor.Direccion, proveedor.Telefono)
            cursor.execute(cls._INSERTAR,valores)
            return cursor.rowcount
    @classmethod
    def actualizar(cls,proveedor):
        with CursorDelPool() as cursor:
            valores = (proveedor.Nombre, proveedor.RFC, proveedor.Direccion, proveedor.Telefono, proveedor.Id)
            cursor.execute(cls._ACTUALIZAR,valores)
            return cursor.rowcount
    @classmethod
    def eliminar(cls,proveedor):
        with CursorDelPool() as cursor:
            valores = (proveedor.Id,)
            cursor.execute(cls._ELIMINAR,valores)
            return cursor.rowcount
        
if __name__ == "__main__":
    #insertar
    # proveedor1 = Proveedor(id=2,nombre="caterpilla",rfc="PXDA21231",direccion="Oradel 105", telefono="8673219523")
    # alumnosInsertados = ProveedorDAO.insertar(proveedor1)
    # log.debug(f"proveedor Agregados {alumnosInsertados}")

    # # #actualizar
    # proveedor = Proveedor(nombre="RHEEM",rfc="RHE161323",direccion="Oradel 106",telefono="8676203657",id=2)
    # proveedorActualizado = ProveedorDAO.actualizar(proveedor)
    # log.debug(f"proveedor Actualizados {proveedorActualizado}")

    # # #eliminar
    proveedor = Proveedor(id=2)
    proveedorEliminado = ProveedorDAO.eliminar(proveedor)
    log.debug(f"proveedor Eliminado {proveedorEliminado}")

    #Leer
    proveedor = ProveedorDAO.seleccionar()
    for a in proveedor:
        log.debug(a)