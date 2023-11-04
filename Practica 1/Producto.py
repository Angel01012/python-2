from logger_base import log 

class Producto:
    def __init__(self,id=None, nombre = None, precio = None) -> None:
        self._id = id
        self._nombre = nombre
        self._precio = precio

    def __str__(self) -> str:
        return f"""
        N°Control: {self._id}
        Nombre: {self._nombre}
        Precio: {self._precio}
        """
    
    @property
    def Id(self):
        return self._id
    @Id.setter
    def Id(self,id):
        self._id = id

    @property
    def Nombre(self):
        return self._nombre
    @Nombre.setter
    def nombre(self,nombre):
        self._nombre = nombre
    
    
    @property
    def Precio(self):
        return self._precio
    @Precio.setter
    def edad(self,precio):
        self._precio = precio

if __name__== "__main__":
    producto1 = Producto(1,"Memoria sd",28.25)
    log.debug(producto1)