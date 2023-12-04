from flask import Blueprint,request,jsonify,render_template,redirect,url_for,flash,Response
from sqlalchemy import exc
from sqlalchemy.orm import aliased
from models import Servicio,Tipo_Servicio,Tecnico,Cliente
from app import db,bcrypt
from auth import tokenCheck,Verificar,admin
from forms import servicioForm
ClienteAlias = aliased(Cliente)
TecnicoAlias = aliased(Tecnico)
Tipo_ServicioAlias = aliased(Tipo_Servicio)
appservicio = Blueprint('appservicio',__name__,template_folder="templates")
@appservicio.route('/')
@tokenCheck
def inicio():
    ad = admin()

    return render_template("index.html",exit=True,admon=ad)

@appservicio.route('/listadoservicios')
@tokenCheck
def listado_servicios(data=None):
    
    serviciocompuesto = db.session.query(Servicio, Tipo_Servicio, Tecnico, Cliente).join(Tipo_ServicioAlias, Servicio.tipo_servicio_id == Tipo_ServicioAlias.id).join(TecnicoAlias, Servicio.tecnico_id == TecnicoAlias.id).join(ClienteAlias, Servicio.cliente_id == ClienteAlias.id).filter(Servicio.cliente_id == Cliente.id, Servicio.tecnico_id == Tecnico.id, Servicio.tipo_servicio_id == Tipo_Servicio.id).all()
    servicios = []
    for servicio,tipo_servicio,tecnico,cliente in serviciocompuesto:
        nuevoservicio = Servicio(id=servicio.id,concepto=servicio.concepto,costo=servicio.costo,status=servicio.status,tecnico_id=tecnico.nombre,tipo_servicio_id=tipo_servicio.nombre,cliente_id=cliente.nombre,registered_input=servicio.registered_input)
        servicios.append(nuevoservicio)
        exit = True
        ad = admin()
    return render_template('listservicios.html',servicios=servicios,exit=exit,admon=ad)

@appservicio.route('/agregarservicio',methods = ["POST","GET"])
@tokenCheck
def agregar_servicio(data=None):
    if request.method == "POST":
        concepto = request.form.get('concepto')
        costo = request.form.get('costo')
        tipo_servicio_id = request.form.get('tipo_servicio_id')
        cliente_id = request.form.get('cliente_id')
        tecnico_id = request.form.get('tecnico_id')
        nuevoservicio = Servicio(concepto=concepto,costo=costo,status="Activo",tecnico_id=tecnico_id,tipo_servicio_id=tipo_servicio_id,cliente_id=cliente_id)
        db.session.add(nuevoservicio)
        db.session.commit()
        return redirect(url_for('appservicio.listado_servicios'))
    else:
        ad = admin()
        tipo_servicios = Tipo_Servicio.query.all()
        clientes = Cliente.query.all()
        tecnicos = Tecnico.query.all()
        return render_template('postservicios.html',tipo_servicios=tipo_servicios,clientes=clientes,tecnicos=tecnicos,exit=True,admon=ad)

@appservicio.route('/detalleservicio/<int:id>')
@tokenCheck
def detalle_servicio(servicio_data,id):
        ad = admin()
        servicio = Servicio.query.get_or_404(id)
        serviciocompuesto = db.session.query(Servicio, Tipo_Servicio, Tecnico, Cliente).join(Tipo_ServicioAlias, Servicio.tipo_servicio_id == Tipo_ServicioAlias.id).join(TecnicoAlias, Servicio.tecnico_id == TecnicoAlias.id).join(ClienteAlias, Servicio.cliente_id == ClienteAlias.id).filter(Servicio.cliente_id == Cliente.id, Servicio.tecnico_id == Tecnico.id, Servicio.tipo_servicio_id == Tipo_Servicio.id,Servicio.id == id).first()
        #print(serviciocompuesto)
        consultarservicio = Servicio(id=serviciocompuesto[0].id,concepto=serviciocompuesto[0].concepto,costo=serviciocompuesto[0].costo,status=serviciocompuesto[0].status,tecnico_id=serviciocompuesto[2].nombre,tipo_servicio_id=serviciocompuesto[1].nombre,cliente_id=serviciocompuesto[3].nombre,registered_input=serviciocompuesto[0].registered_input)
        consultarcliente = Cliente(id=serviciocompuesto[3].id,nombre=serviciocompuesto[3].nombre,telefono=serviciocompuesto[3].telefono,email=serviciocompuesto[3].email,direccion=serviciocompuesto[3].direccion,RFC=serviciocompuesto[3].RFC,tipoCliente=serviciocompuesto[3].tipo_clientes_id)
        consultartecnico = Tecnico.query.get_or_404(servicio.cliente_id)
        #print(consultarservicio)
        return render_template('getservicios.html',servicio=consultarservicio,cliente=consultarcliente,tecnico=consultartecnico,exit=True,admon=ad)


@appservicio.route('/modificarservicio/<int:id>',methods = ["POST","GET"])
@tokenCheck
def modificar_servicio(servicio_data,id):
    ad = admin()
    print(ad)
    servicio = Servicio.query.get_or_404(id)
    formaSericio = servicioForm(obj=servicio)
    if request.method == "POST":
        formaSericio.populate_obj(servicio)
        db.session.commit()
        return redirect(url_for('appservicio.listado_servicios'))
    tipo_servicios = Tipo_Servicio.query.all()
    clientes = Cliente.query.all()
    tecnicos = Tecnico.query.all()
    return render_template('putservicios.html',servicio=servicio,tipo_servicios=tipo_servicios,clientes=clientes,tecnicos=tecnicos,exit=True,admon=ad)

def generate_csv():
    # Create a CSV string or generate data dynamically
    csv_data = [
        #['Name', 'Age', 'Country'],
        #['John', '25', 'USA'],
        #['Alice', '30', 'Canada'],
        #['Bob', '28', 'UK']
    ]
    
    serviciocompuesto = db.session.query(Servicio, Tipo_Servicio, Tecnico, Cliente).join(Tipo_ServicioAlias, Servicio.tipo_servicio_id == Tipo_ServicioAlias.id).join(TecnicoAlias, Servicio.tecnico_id == TecnicoAlias.id).join(ClienteAlias, Servicio.cliente_id == ClienteAlias.id).filter(Servicio.cliente_id == Cliente.id, Servicio.tecnico_id == Tecnico.id, Servicio.tipo_servicio_id == Tipo_Servicio.id).all()
    csv_data.append(['id','concepto','costo','status','tecnico','cliente','tipo de servicio','inicio','final'])
    for servicio,tipo_servicio,tecnico,cliente in serviciocompuesto:
        id = servicio.id
        concepto = servicio.concepto
        costo = servicio.costo
        status = servicio.status
        tecnico_nombre = tecnico.nombre
        tipo_service = tipo_servicio.nombre
        cliente_nombre = cliente.nombre
        fechainicio = servicio.registered_input
        if servicio.registered_output == None:
            fechafinal = '0000-00-00'
        else:
            fechafinal = servicio.registered_output
            pass

        nuevoservicio = Servicio(id=servicio.id,concepto=servicio.concepto,costo=servicio.costo,status=servicio.status,tecnico_id=tecnico.nombre,tipo_servicio_id=tipo_servicio.nombre,cliente_id=cliente.nombre,registered_input=servicio.registered_input)
        #print(nuevoservicio.registered_output)
        #print(csv_data)
        aux = [id,concepto,costo,status,tecnico_nombre,cliente_nombre,tipo_service,fechainicio,fechafinal]
        csv_data.append(aux)
    # Create a generator to yield CSV rows
    print(csv_data)
    def generate():
        for row in csv_data:
            row_str = [str(item) for item in row]
            yield ','.join(row_str) + '\n'
    
    # Set response headers to indicate CSV content
    headers = {
        'Content-Disposition': 'attachment; filename=servicios.csv',
        'Content-Type': 'text/csv'
    }
    
    # Return a Flask response object with the CSV generator
    return Response(generate(), headers=headers)

@appservicio.route('/download-csv')
def descargar_csv():
    return generate_csv()