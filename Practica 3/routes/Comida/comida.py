from flask import Blueprint,request,redirect,render_template,url_for,jsonify
from models import Comida
from forms import ComidaForm
from app import db

appcomida = Blueprint('appcomida',__name__,template_folder="templates")

@appcomida.route('/')
def inicio():
    return render_template("index.html")
@appcomida.route('/listadocomida')
def listadocomida():
    comidas = Comida.query.all()
    return render_template('listadocomida.html',comidas=comidas)

@appcomida.route('/formulariocomida',methods=["GET","POST"])
def formularioproducto():
    comida = Comida()
    comidaform = ComidaForm(obj=comida)
    if request.method == "POST":
        if comidaform.validate_on_submit():
            comidaform.populate_obj(comida)
            db.session.add(comida)
            db.session.commit()
            return redirect(url_for('appcomida.listadocomida'))
    return render_template('formulariocomida.html',forma=comidaform)

@appcomida.route('/editarcomida/<int:id>',methods=["GET","POST"])
def editarcomida(id):
    comida = Comida.query.get_or_404(id)
    comidaform = ComidaForm(obj=comida)
    if request.method == "POST":
        if comidaform.validate_on_submit():
            comidaform.populate_obj(comida)
            db.session.commit()
            return redirect(url_for('appcomida.listadocomida'))
    return render_template('editarcomida.html',forma=comidaform)

@appcomida.route('/consultarcomida/<int:id>',methods=["GET","POST"])
def consultarcomida(id):
    comida = Comida.query.get_or_404(id)
    comidas = [comida]
    #productoform = ProductosForm(obj=producto)
    
    return render_template('consultacomida.html',comidas=comidas)

@appcomida.route('/eliminarcomida/<int:id>', methods=["POST","GET"])
def eliminarcomida(id):
    comida = Comida.query.get_or_404(id)
    db.session.delete(comida)
    db.session.commit()
    return redirect(url_for('appcomida.listadocomida'))

@appcomida.route('/ConsultarTodasComidas',methods=["GET"])
def consultartodas():
    comidas = Comida.query.all()
    cad = ""
    for comida in comidas:
        cad = cad + f"id: {comida.id}, nombre: {comida.nombre}, precio: {comida.precio}" 
    respuesta =  jsonify(cad)
    return respuesta

@appcomida.route('/ConsultarUnaComida',methods=["GET"])
def consultarunocomida():
    json = request.get_json()
    comida = Comida.query.get_or_404(json["id"])
    cad = f"id: {comida.id}, nombre: {comida.nombre}, precio: {comida.precio}"
    respuesta = jsonify(cad)
    return respuesta

@appcomida.route('/AgregarComida',methods=["POST"])
def agregarcomida():
    json = request.get_json()
    comida = Comida()
    comida.precio = json["precio"]
    comida.nombre = json["nombre"]
    db.session.add(comida)
    db.session.commit()
    respuesta = jsonify({"status":200,"mensaje":"comida agregada"})
    return respuesta

@appcomida.route('/EditarComida',methods = ["PUT"])
def Editarcomida():
    json = request.get_json()
    comida = Comida.query.get_or_404(json["id"])
    comida.precio = json["precio"]
    comida.nombre = json["nombre"]
    db.session.commit()
    respuesta = jsonify({"status":200,"mensaje":"comida editada"})
    return respuesta

@appcomida.route('/BorrarComida',methods=["DELETE"])
def borrarcomida():
    json = request.get_json()
    comida = Comida.query.get_or_404(json["id"])
    db.session.delete(comida)
    db.session.commit()
    respuesta = jsonify({"status":200,"mensaje":"comida eliminada"})
    return respuesta