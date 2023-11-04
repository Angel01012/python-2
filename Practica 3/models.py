from app import db
from sqlalchemy import Numeric

#formulario
class Cliente(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))

#JSON
class Producto(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Numeric(10, 2))
    nombre = db.Column(db.String(250))

#formularios
class Comida(db.Model):
    __tablename__ = "comida"
    id = db.Column(db.Integer,primary_key=True)
    precio = db.Column(db.Numeric(10, 2))
    nombre = db.Column(db.String(250))
