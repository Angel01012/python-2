from django.db import models

# Create your models here.
class Domicilio(models.Model):
    calle = models.CharField(max_length=255)
    no_calle= models.IntegerField()
    pais = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f"Calle: {self.calle}, No Calle: {self.no_calle}, pais: {self.pais}"

class Editorial(models.Model):
    editorial = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f"Editorial: {self.editorial}"

class Autor(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}"
    
class Categoria(models.Model):
    descripcion = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f"Descripcion: {self.descripcion}"

class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    edicion = models.CharField(max_length=255)
    editorial = models.ForeignKey(Editorial,on_delete=models.SET_NULL,null=True)
    autor = models.ForeignKey(Autor,on_delete=models.SET_NULL,null=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.SET_NULL,null=True)
    def __str__(self) -> str:
        return f"Titulo: {self.titulo}, Edicion: {self.edicion}, Editorial: {self.editorial}, Autor: {self.autor}, Categoria: {self.categoria}"
 
class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    domicilio = models.ForeignKey(Domicilio,on_delete=models.SET_NULL,null=True)
    def __str__(self) -> str:
        return f"Cliente: {self.id}, Nombre completo: {self.nombre}, email: {self.email}, domicilio {self.domicilio}"