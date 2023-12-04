from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class rolForm(FlaskForm):
    nombre = StringField('nombre')

class tecnicoForm(FlaskForm):
    nombre = StringField('nombre')
    apellido = StringField('apellido')

class userForm(FlaskForm):
    email = StringField('email')
    password = StringField('password')
    tecnico_id = StringField('tecnico_id')
    rol_id = StringField('rol_id')


class tiposervicioForm(FlaskForm):
    nombre = StringField('nombre')

class servicioForm(FlaskForm):
    concepto = StringField('concepto')
    costo = StringField('costo')
    tecnico_id = StringField('tecnico_id')
    tipo_servicio_id = StringField('tipo_servicio_id') 
    cliente_id = StringField('cliente_id')

class tipoclienteForm(FlaskForm):
    nombre = StringField('nombre')

class clienteForm(FlaskForm):
    nombre = StringField('nombre')
    telefono = StringField('telefono')
    email = StringField('email')
    direccion = StringField('direccion')
    RFC = StringField('RFC')
    tipo_clientes_id = StringField('tipo_clientes_id')

