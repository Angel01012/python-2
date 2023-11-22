from flask import Blueprint,request,redirect,render_template,url_for,jsonify
from models import Cliente
from forms import clienteForm
from app import db

appcliente = Blueprint('appcliente',__name__,template_folder="templates")

@appcliente.route('/')
def inicio():
    return render_template("inicio.html")
@appcliente.route('/listadoCliente')
def listadocliente():
    cliente = Cliente.query.all()
    return render_template('listadoCliente.html',cliente=cliente)

@appcliente.route('/formularioCliente',methods=["GET","POST"])
def formularioCliente():
    cliente = Cliente()
    clienteform = clienteForm(obj=cliente)
    if request.method == "POST":
        if clienteform.validate_on_submit():
            clienteform.populate_obj(cliente)
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('appcliente.listadoCliente'))
    return render_template('formularioCliente.html',forma=clienteform)

@appcliente.route('/editarCliente/<int:id>',methods=["GET","POST"])
def editarCliente(id):
    cliente = Cliente.query.get_or_404(id)
    clienteform = clienteForm(obj=cliente)
    if request.method == "POST":
        if clienteform.validate_on_submit():
            clienteform.populate_obj(cliente)
            db.session.commit()
            return redirect(url_for('appcliente.listadoCliente'))
    return render_template('editarCliente.html',forma=clienteform)

@appcliente.route('/consultarCliente/<int:id>',methods=["GET","POST"])
def consultarCliente(id):
    cliente = Cliente.query.get_or_404(id)
    clientes = [cliente]
    
    return render_template('consultaCliente.html',clientes=cliente)

@appcliente.route('/eliminarCliente/<int:id>', methods=["POST","GET"])
def eliminarCliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('appcliente.listadoCliente'))