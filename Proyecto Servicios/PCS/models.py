from app import db
from sqlalchemy import Numeric
import jwt
import datetime
from config import BaseConfig
from app import db,bcrypt

#tabla ROL

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(30))

#tabla Tecnico
class Tecnico(db.Model):
    __tablename__="tecnico"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(55))
    apellido = db.Column(db.String(55))

#usuario
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    registered_on=db.Column(db.DateTime,nullable=False)
    admin=db.Column(db.Boolean,nullable=False,default=False)

    def __init__(self,email,password,admin=False) -> None:
        self.email=email
        self.password=bcrypt.generate_password_hash(
            password,BaseConfig.BCRYPT_LOG_ROUNDS
        ).decode()

        self.registered_on=datetime.datetime.now()
        self.admin=admin

    def encode_auth_token(self,user_id):
        try:
            print('USER',user_id)
            payload={
                'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=5),
                'iat':datetime.datetime.utcnow(),
                'sub':user_id
            }
            print("PAYLOAD",payload)
            return jwt.encode(
                payload,
                BaseConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            print("EXCEPTION")
            print(e)
            return e
        
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,BaseConfig.SECRET_KEY,algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError as e:
            return 'Signature Expired Please log in again'

        except jwt.InvalidTokenError as e:
            return 'Invalid token'

#Tipo Servicios
class Tipo_Servicio(db.Model):
    __tablename__="tipo_servicio"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)

#Servicios
class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    concepto = db.Column(db.String(255))
    registered_input=db.Column(db.DateTime,nullable=False)
    costo = db.Column(db.Numeric(10, 2))
    registered_output=db.Column(db.DateTime,nullable=False)
    tecnico_id=db.Column(db.Integer,db.ForeignKey('tecnico.id'))
    tipo_servicio_id=db.Column(db.Integer,db.ForeignKey('tipo_servicio.id'))

#tipoClientes
class Tipo_Cliente(db.Model):
    __tablename__="tipo_cliente"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
#Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80),unique=True,nullable=False)
    telefono = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(120),unique=True)
    direccion = db.Column(db.String(300))
    RFC = db.Column(db.String(30),unique = True)
    tipo_clientes_id=db.Column(db.Integer,db.ForeignKey('tipo_cliente.id'))
