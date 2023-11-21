from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms .validators import DataRequired

class ProductosForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired()])
    descripcion = StringField('descripcion')
    precio = StringField('precio',validators=[DataRequired()])
    enviar = SubmitField("Enviar")

class ComidaForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired()])
    precio = StringField('precio',validators=[DataRequired()])
    enviar = SubmitField("Enviar")