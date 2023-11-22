from flask import Blueprint,request,jsonify,render_template,redirect,url_for
from sqlalchemy import exc
from models import Tecnico
from app import db,bcrypt
from auth import tokenCheck,Verificar
from forms import tecnicoForm

apptecnico=Blueprint('apptecnico',__name__,template_folder="templates")

@apptecnico.route('/')
def inicio():
    render_template("index.html")

@apptecnico.route('/listadotecnicos')
def listado_tecnicos():
    tecnicos = Tecnico.query.all()
    return render_template('listtecnicos.html',tecnicos=tecnicos)

@apptecnico.route('/agregartecnico',methods=["POST","GET"])
def agregar_tecnico():

    if request.method == "POST":
        Nombre = request.form.get('nombre')
        Apellido = request.form.get('apellido')
        print(Nombre,Apellido)
        tecniconuevo = Tecnico(nombre=Nombre,apellido=Apellido)
        db.session.add(tecniconuevo)
        db.session.commit()
        return redirect(url_for('apptecnico.listado_tecnicos'))
    else:
        return render_template('posttecnicos.html')

@apptecnico.route('/detallestecnico/<int:id>')
def detalles_tecnico(id):
    tecnico = Tecnico.query.get_or_404(id)
    tecnicos = [tecnico]
    return render_template('gettecnicos.html',tecnicos=tecnicos)
    pass

@apptecnico.route('/modificartecnico/<int:id>',methods=["POST","GET"])
def modificar_tecnico(id):
    tecnico = Tecnico.query.get_or_404(id)
    formatecnico = tecnicoForm(obj=tecnico)
    if request.method == "POST":
        formatecnico.populate_obj(tecnico)
        db.session.commit()
        return redirect(url_for('apptecnico.listado_tecnicos'))
    return render_template('puttecnicos.html',tecnico = tecnico)

@apptecnico.route('/modificartecnico',methods=["POST"])
def modificarformu():
    pass