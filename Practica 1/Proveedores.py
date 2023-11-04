from logger_base import log 

class Proveedor:
    def __init__(self,id=None, nombre = None, rfc = None, direccion = None, telefono = None) -> None:
        self._id = id
        self._nombre = nombre
        self._rfc = rfc
        self._direccion = direccion
        self._telefono = telefono
    
    def __str__(self) -> str:
        return f"""
        id: {self._id}
        Nombre: {self._nombre}
        RFC: {self._rfc}
        Direccion: {self._direccion}
        Telefono: {self._telefono}
        """
    
    @property
    def Id(self):
        return self._id
    @Id.setter
    def Id(self,Id):
        self._id = Id

    @property
    def Nombre(self):
        return self._nombre
    @Nombre.setter
    def nombre(self,nombre):
        self._nombre = nombre
    
    @property
    def RFC(self):
        return self._rfc
    @RFC.setter
    def rfc(self,rfc):
        self._rfc = rfc
    
    @property
    def Direccion(self):
        return self._direccion
    @Direccion.setter
    def direccion(self,direccion):
        self._direccion = direccion

    @property
    def Telefono(self):
        return self._telefono
    @Telefono.setter
    def telefono(self,telefono):
        self._telefono = telefono
if __name__== "__main__":
    proveedor1 = Proveedor(1,"Juan","miRfc","lago de chapala #255","8672820012")
    log.debug(proveedor1)