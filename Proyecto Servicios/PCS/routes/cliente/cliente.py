import csv
from werkzeug.utils import secure_filename
from flask import Blueprint,request,jsonify,render_template,redirect,url_for,Response
from sqlalchemy import exc
from models import Cliente,Tipo_Cliente
from app import db,bcrypt
from auth import tokenCheck,Verificar,admin
from forms import clienteForm
from io import StringIO

appcliente=Blueprint('appcliente',__name__,template_folder="templates")


@appcliente.route('/')
@tokenCheck
def inicio():
    ad = admin()
    return render_template("index.html",exit=True,admon=ad)

@appcliente.route('/listadocliente')
@tokenCheck
def listado_clientes(data=None):
    ad = admin()
    resultado = db.session.query(Cliente, Tipo_Cliente).join(Tipo_Cliente).filter(Cliente.tipo_clientes_id == Tipo_Cliente.id).order_by(Cliente.id).all()    
    Clientes = []
    for cliente,tipo_cliente in resultado:
        nuevocliente = Cliente(id=cliente.id,nombre=cliente.nombre,telefono=cliente.telefono,email=cliente.email,direccion=cliente.direccion,RFC=cliente.RFC,tipoCliente=tipo_cliente.nombre)
        Clientes.append(nuevocliente)
    return render_template('listcliente.html',clientes=Clientes,exit=True,admon=ad)

@appcliente.route('/agregarcliente',methods=["POST","GET"])
@tokenCheck
def agregar_cliente(data=None):
    ad = admin()
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
        return render_template('postcliente.html',tipo_clientes = Tipo_Clientes,exit=True,admon=ad)

@appcliente.route('/detallescliente/<int:id>')
@tokenCheck
def detalles_cliente(cliente_data,id):
    ad = admin()
    cliente = Cliente.query.get_or_404(id)
    resultado = db.session.query(Cliente, Tipo_Cliente).join(Tipo_Cliente).filter(Cliente.id == cliente.id).first()    
    
    
    nuevocliente = Cliente(id=resultado[0].id,nombre=resultado[0].nombre,telefono=resultado[0].telefono,email=resultado[0].email,direccion=resultado[0].direccion,RFC=resultado[0].RFC,tipoCliente=resultado[1].nombre)
    Clientes = [nuevocliente]
    return render_template('getcliente.html',cliente=nuevocliente,exit=True,admon=ad)

@appcliente.route('/modificarcliente/<int:id>',methods=["POST","GET"])
@tokenCheck
def modificar_cliente(cliente_data,id):
    ad = admin()
    cliente = Cliente.query.get_or_404(id)
    print(cliente)
    formacliente = clienteForm(obj=cliente)
    if request.method == "POST":
        formacliente.populate_obj(cliente)
        db.session.commit()
        return redirect(url_for('appcliente.listado_clientes'))
    Tipo_Clientes = Tipo_Cliente.query.all()
    return render_template('putcliente.html',cliente = cliente,tipo_clientes = Tipo_Clientes,exit=True,admon=ad)

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

def process_csv_content(content):
    csv_reader = csv.reader(content)
    # Skip the header row
    next(csv_reader)
    for row in csv_reader:
        # Assuming the CSV columns order matches the order in the database model
        nombre,telefono,email,direccion,RFC,tipo_cliente_id = row
        # Convert necessary fields to appropriate types (e.g., int, float, datetime)
        # ...

        # Create a new Servicio instance and insert it into the database
        nuevo_cliente = Cliente(nombre=nombre,telefono=telefono,email=email,direccion=direccion,RFC=RFC,tipoCliente=tipo_cliente_id)
        db.session.add(nuevo_cliente)

    # Commit changes to the database
    db.session.commit()

@appcliente.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Assuming the file is sent as part of the POST request
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        # Read the content of the uploaded file
        file_content = file.read().decode('utf-8')
        # Use StringIO to create a file-like object in memory
        csv_content = StringIO(file_content)
        # Process the CSV content and insert rows into the database
        process_csv_content(csv_content)
        # Return a response indicating success
        return redirect(url_for('appcliente.listado_clientes'))
    else:
        # Return an error response if the uploaded file is not a CSV
        return redirect(url_for('appcliente.listado_clientes'))