from app import db
from sqlalchemy import Numeric
import jwt
import datetime
from config import BasicConfig
from app import db,bcrypt

#tabla ROL

class Rol(db.Model):
    __tablename__="rol"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(30))

#tabla Tecnico
class Tecnico(db.Model):
    __tablename__="tecnico"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(55))
    apellido = db.Column(db.String(55))
    def __init__(self,nombre,apellido) -> None:
        self.nombre = nombre
        self.apellido = apellido

#usuario
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    registered_on=db.Column(db.DateTime,nullable=False)
    admin=db.Column(db.Boolean,nullable=False,default=False)
    tecnico_id=db.Column(db.Integer,db.ForeignKey('tecnico.id'))
    rol_id = db.Column(db.Integer,db.ForeignKey('rol.id'))

    def __init__(self,email,password,tecnicoid,rolid,admin=False) -> None:
        self.email=email
        self.tecnico_id = tecnicoid
        self.rol_id = rolid
        self.password=bcrypt.generate_password_hash(
            password,BasicConfig.BCRYPT_LOG_ROUNDS
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
                BasicConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            print("EXCEPTION")
            print(e)
            return e
        
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,BasicConfig.SECRET_KEY,algorithms=['HS256'])
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
    status = db.Column(db.String(255))
    registered_output=db.Column(db.DateTime)
    tecnico_id=db.Column(db.Integer,db.ForeignKey('tecnico.id'))
    tipo_servicio_id=db.Column(db.Integer,db.ForeignKey('tipo_servicio.id'))
    cliente_id = db.Column(db.Integer,db.ForeignKey('cliente.id'))

    def __init__(self,concepto,costo,status,tecnico_id,tipo_servicio_id,cliente_id,id=None) -> None:
        if id ==None:
            pass
        else:
            self.id = id
        self.concepto = concepto
        self.costo = costo
        self.status = status
        self.registered_input=datetime.datetime.now()
        self.tecnico_id = tecnico_id
        self.tipo_servicio_id = tipo_servicio_id
        self.cliente_id = cliente_id

    def __str__(self) -> str:
        return f"id:{self.id} concepto:{self.concepto} costo:{self.costo} status:{self.status} registro entrada:{self.registered_input} tecnico:{self.tecnico_id} cliente:{self.cliente_id} tipo de servicio:{self.tipo_servicio_id}"
#tipoClientes
class Tipo_Cliente(db.Model):
    __tablename__="tipo_cliente"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
#Clientes
class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80),unique=True,nullable=False)
    telefono = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(120),unique=True)
    direccion = db.Column(db.String(300))
    RFC = db.Column(db.String(30),unique = True)
    tipo_clientes_id=db.Column(db.Integer,db.ForeignKey('tipo_cliente.id'))
    def __init__(self, nombre, telefono, email, direccion, RFC, tipoCliente, id=None) -> None:
        if id == None:
            pass
        else:
            self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.RFC = RFC
        self.tipo_clientes_id = tipoCliente

    def __str__(self) -> str:
        return f"nombre: {self.nombre} telefono: {self.telefono}, email: {self.email}, direccion: {self.direccion}, RFC: {self.RFC}, TipodeCliente: {self.tipo_clientes_id}"

class Images(db.Model):
    __tablename__ = 'user_images'
    id_images = db.Column(db.Integer,primary_key =True)
    type = db.Column(db.String(255),nullable=False)
    data = db.Column(db.LargeBinary,nullable=False)
    rendered_data = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    region = db.relationship('User',backref='users')