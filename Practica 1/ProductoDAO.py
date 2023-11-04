from Producto import Producto 
from cursorDelPool import CursorDelPool
from Conexion import Conexion
from logger_base import log

class ProductoDAO:
    _SELECCIONAR = "SELECT * FROM producto ORDER BY id"
    _INSERTAR = "INSERT INTO producto (id,nombre,precio) VALUES (%s,%s,%s)"
    _ACTUALIZAR = "UPDATE producto SET nombre=%s,precio=%s WHERE id=%s"
    _ELIMINAR = "DELETE FROM producto WHERE id=%s"

    @classmethod
    def seleccionar(cls):
        with CursorDelPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            productos = []
            for r in registros:
                producto = Producto(r[0],r[1],r[2])
                productos.append(producto)
            return productos
    @classmethod
    def insertar(cls,producto):
        with CursorDelPool() as cursor:
            valores = (producto.Id,producto.Nombre, producto.Precio)
            cursor.execute(cls._INSERTAR,valores)
            return cursor.rowcount
    @classmethod
    def actualizar(cls,producto):
        with CursorDelPool() as cursor:
            valores = (producto.Nombre, producto.Precio, producto.Id)
            cursor.execute(cls._ACTUALIZAR,valores)
            return cursor.rowcount
    @classmethod
    def eliminar(cls,producto):
        with CursorDelPool() as cursor:
            valores = (producto.Id,)
            cursor.execute(cls._ELIMINAR,valores)
            return cursor.rowcount
        
if __name__ == "__main__":
    # #insertar
    producto1 = Producto(id=3,nombre="SSD 128",precio=60.20)
    alumnosInsertados = ProductoDAO.insertar(producto1)
    log.debug(f"producto Agregado {alumnosInsertados}")

    # # #actualizar
    producto = Producto(nombre="Adaptador wifi",precio=28.10,id=3)
    productoActualizado = ProductoDAO.actualizar(producto)
    log.debug(f"Producto Actualizados {productoActualizado}")

    # # #eliminar
    producto = Producto(id=3)
    productoEliminado = ProductoDAO.eliminar(producto)
    log.debug(f"Producto Eliminados {productoEliminado}")

    #Leer
    producto = ProductoDAO.seleccionar()
    for a in producto:
        log.debug(a)