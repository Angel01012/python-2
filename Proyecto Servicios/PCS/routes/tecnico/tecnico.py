from flask import Blueprint,request,jsonify,render_template,redirect,url_for
from sqlalchemy import exc
from models import Tecnico,User
from app import db,bcrypt
from auth import tokenCheck,Verificar,obtenerInfo,admin
from forms import tecnicoForm

apptecnico=Blueprint('apptecnico',__name__,template_folder="templates")


@apptecnico.route('/')
@tokenCheck
def inicio(data=None):
    ad = admin()
    return render_template("main.html",exit=True,admon=ad)

@apptecnico.route('/listadotecnicos')
@tokenCheck
def listado_tecnicos(data=None):
    ad = admin()
    tecnicos = Tecnico.query.all()
    return render_template('listtecnicos.html',tecnicos=tecnicos,admon=ad,exit=True)

@apptecnico.route('/agregartecnico',methods=["POST","GET"])
@tokenCheck
def agregar_tecnico(data=None):
    
    ad = admin()

    if request.method == "POST":
        Nombre = request.form.get('nombre')
        Apellido = request.form.get('apellido')
        tecniconuevo = Tecnico(nombre=Nombre,apellido=Apellido)
        db.session.add(tecniconuevo)
        db.session.commit()
        return redirect(url_for('apptecnico.listado_tecnicos'))
    else:
        return render_template('posttecnicos.html',exit=True)

@apptecnico.route('/detallestecnico/<int:id>')
@tokenCheck
def detalles_tecnico(tecnico_data,id):
    ad = admin()

    tecnico = Tecnico.query.get_or_404(id)
    tecnicos = [tecnico]
    return render_template('gettecnicos.html',tecnico=tecnico,exit=True,admon=ad)

@apptecnico.route('/modificartecnico/<int:id>',methods=["POST","GET"])
@tokenCheck
def modificar_tecnico(tecnico_data,id):
    ad = admin()

    tecnico = Tecnico.query.get_or_404(id)
    formatecnico = tecnicoForm(obj=tecnico)
    if request.method == "POST":
        formatecnico.populate_obj(tecnico)
        db.session.commit()
        return redirect(url_for('apptecnico.listado_tecnicos'))
    return render_template('puttecnicos.html',tecnico = tecnico,exit=True)