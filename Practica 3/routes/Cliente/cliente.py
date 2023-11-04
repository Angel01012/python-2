from flask import Blueprint,request,redirect,render_template,url_for,jsonify
from models import Cliente
from app import db

appcliente = Blueprint('appcliente',__name__,template_folder="templates")

@appcliente.route('/')
def inicio():
    return render_template("index.html")

@appcliente.route('/ConsultarTodos',methods=["GET"])
def consultartodos():
    json = request.get_json()
    clientes = Cliente.query.all()
    cad = ""
    for cliente in clientes:
        cad = cad + f"id: {cliente.id}, nombre: {cliente.nombre}, apellido: {cliente.apellido}, email: {cliente.email}" 

    respuesta =  jsonify(cad)
    return respuesta

@appcliente.route('/ConsultarUno',methods=["GET"])
def consultaruno():
    json = request.get_json()
    cliente = Cliente.query.get_or_404(json["id"])
    cad = f"id: {cliente.id}, nombre: {cliente.nombre}, apellido: {cliente.apellido}, email: {cliente.email}"
    respuesta = jsonify(cad)
    return respuesta

@appcliente.route('/AgregarCliente',methods=["POST"])
def agregarcliente():
    json = request.get_json()
    cliente = Cliente()
    cliente.nombre = json["nombre"]
    cliente.email = json["email"]
    cliente.apellido = json["apellido"]
    db.session.add(cliente)
    db.session.commit()
    respuesta = jsonify({"status":200,"mensaje":"cliente agregado"})
    return respuesta

@appcliente.route('/EditarCliente',methods = ["PUT"])
def editarcliente():
    json = request.get_json()
    cliente = Cliente.query.get_or_404(json["id"])
    cliente.email = json["email"]
    cliente.nombre = json["nombre"]
    cliente.apellido = json["apellido"]
    db.session.commit()
    respuesta = jsonify({"status":200,"mensaje":"cliente editado"})
    return respuesta

@appcliente.route('/BorrarCliente',methods=["DELETE"])
def borrarcliente():
    json = request.get_json()
    cliente = Cliente.query.get_or_404(json["id"])
    db.session.delete(cliente)
    db.session.commit()
    respuesta = jsonify({"status":200,"mensaje":"cliente eliminado"})
    return respuesta