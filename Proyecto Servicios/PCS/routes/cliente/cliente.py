from flask import Blueprint,request,jsonify,render_template,redirect,url_for,flash
from sqlalchemy import exc
from models import Cliente,Tipo_Cliente
from app import db,bcrypt
from auth import tokenCheck,Verificar
from forms import clienteForm

appcliente=Blueprint('appcliente',__name__,template_folder="templates")

@appcliente.route('/')
def inicio():
    return render_template("index.html")

@appcliente.route('/listadocliente')
def listado_clientes():
    resultado = db.session.query(Cliente, Tipo_Cliente).join(Tipo_Cliente).filter(Cliente.tipo_clientes_id == Tipo_Cliente.id).all()    
    Clientes = []
    for cliente,tipo_cliente in resultado:
        nuevocliente = Cliente(id=cliente.id,nombre=cliente.nombre,telefono=cliente.telefono,email=cliente.email,direccion=cliente.direccion,RFC=cliente.RFC,tipoCliente=tipo_cliente.nombre)
        Clientes.append(nuevocliente)
    return render_template('listcliente.html',clientes=Clientes)

@appcliente.route('/agregarcliente',methods=["POST","GET"])
def agregar_cliente():
    if request.method == "POST":
        Nombre = request.form.get('nombre')
        Telefono = request.form.get('telefono')
        Email = request.form.get('email')
        Direccion = request.form.get('direccion')
        RFC = request.form.get('RFC')
        TipoCliente = request.form.get('tipo_clientes_id')
        print(Nombre,Email,Telefono,RFC,Direccion,TipoCliente)
        clientenuevo = Cliente(nombre=Nombre,telefono=Telefono,email=Email,direccion=Direccion,RFC=RFC,tipoCliente=TipoCliente)
        db.session.add(clientenuevo)
        db.session.commit()
        return redirect(url_for('appcliente.listado_clientes'))
    else:
        Tipo_Clientes = Tipo_Cliente.query.all()
        print(Tipo_Clientes)
        return render_template('postcliente.html',tipo_clientes = Tipo_Clientes)

@appcliente.route('/detallescliente/<int:id>')
def detalles_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    resultado = db.session.query(Cliente, Tipo_Cliente).join(Tipo_Cliente).filter(Cliente.id == cliente.id).first()    
    print("consultar uno ",resultado)
    
    nuevocliente = Cliente(id=resultado[0].id,nombre=resultado[0].nombre,telefono=resultado[0].telefono,email=resultado[0].email,direccion=resultado[0].direccion,RFC=resultado[0].RFC,tipoCliente=resultado[1].nombre)
    Clientes = [nuevocliente]
    return render_template('getcliente.html',clientes=Clientes)

@appcliente.route('/modificarcliente/<int:id>',methods=["POST","GET"])
def modificar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    print(cliente)
    #resultado = db.session.query(Cliente, Tipo_Cliente).join(Tipo_Cliente).filter(Cliente.id == cliente.id).first()
    formacliente = clienteForm(obj=cliente)
    if request.method == "POST":
        formacliente.populate_obj(cliente)
        db.session.commit()
        #flash('You were successfully logged in')
        return redirect(url_for('appcliente.listado_clientes'))
    Tipo_Clientes = Tipo_Cliente.query.all()
    #nuevocliente = Cliente(id=resultado[0].id,nombre=resultado[0].nombre,telefono=resultado[0].telefono,email=resultado[0].email,direccion=resultado[0].direccion,RFC=resultado[0].RFC,tipoCliente=resultado[1].nombre)
    return render_template('putcliente.html',cliente = cliente,tipo_clientes = Tipo_Clientes)

@appcliente.route('/testjoin')
def test():
    resultado = db.session.query(Cliente, Tipo_Cliente).join(Tipo_Cliente).filter(Cliente.tipo_clientes_id == Tipo_Cliente.id).all()    
    print(resultado)
    Clientes = []
    for cliente,tipo_cliente in resultado:
        nuevocliente = Cliente(id=cliente.id,nombre=cliente.nombre,telefono=cliente.telefono,email=cliente.email,direccion=cliente.direccion,RFC=cliente.RFC,tipoCliente=tipo_cliente.nombre)
        Clientes.append(nuevocliente)
    #nuevocliente = Cliente(id=resultado[0].id,nombre=resultado[0].nombre,telefono=resultado[0].telefono,email=resultado[0].email,direccion=resultado[0].direccion,RFC=resultado[0].RFC,tipoCliente=resultado[1].nombre)
    print(Clientes)
    respuesta = jsonify({"res": "200"})
    return respuesta
