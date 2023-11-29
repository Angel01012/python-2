from flask import Blueprint,request,jsonify,render_template,redirect,url_for,flash
from sqlalchemy import exc
from sqlalchemy.orm import aliased
from models import Servicio,Tipo_Servicio,Tecnico,Cliente
from app import db,bcrypt
from auth import tokenCheck,Verificar
from forms import servicioForm

appservicio = Blueprint('appservicio',__name__,template_folder="templates")
@appservicio.route('/')
def inicio():
    return render_template("index.html")

@appservicio.route('/listadoservicios')
def listado_servicios():
    ClienteAlias = aliased(Cliente)
    TecnicoAlias = aliased(Tecnico)
    Tipo_ServicioAlias = aliased(Tipo_Servicio)
    #servicioCompuesto1 = db.session.query(Servicio,Tipo_Servicio,Tecnico,Cliente).join(Tipo_Servicio,Tecnico,Cliente).filter(Servicio.cliente_id == Cliente.id and Servicio.tecnico_id == Tecnico.id and Servicio.tipo_servicio_id == Tipo_Servicio.id).all()    
    #servicioCompuesto = db.session.query(Servicio,Tipo_Servicio,Tecnico,Cliente).join(Tipo_Servicio).filter(Cliente.tipo_clientes_id == Tipo_Cliente.id).all()
    serviciocompuesto = db.session.query(Servicio, Tipo_Servicio, Tecnico, Cliente).join(Tipo_ServicioAlias, Servicio.tipo_servicio_id == Tipo_ServicioAlias.id).join(TecnicoAlias, Servicio.tecnico_id == TecnicoAlias.id).join(ClienteAlias, Servicio.cliente_id == ClienteAlias.id).filter(Servicio.cliente_id == Cliente.id, Servicio.tecnico_id == Tecnico.id, Servicio.tipo_servicio_id == Tipo_Servicio.id).all()
    print(serviciocompuesto)
    servicios = []
    for servicio,tipo_servicio,tecnico,cliente in serviciocompuesto:
        nuevoservicio = Servicio(id=servicio.id,concepto=servicio.concepto,costo=servicio.costo,status=servicio.status,tecnico_id=tecnico.nombre,tipo_servicio_id=tipo_servicio.nombre,cliente_id=cliente.nombre)
        print(nuevoservicio)
        servicios.append(nuevoservicio)
    print(servicios)
    respuesta = jsonify({"status":"200"})
    return respuesta
    pass

@appservicio.route('/agregarservicio',methods = ["POST","GET"])
def agregar_servicio():
    pass

#@appservicio.route('detalleservicio/<int:id>')
#def detalle_servicio(id):
#    pass

#@appservicio.route('/modificar/<int:id>')
#def modificar_servicio(id):
#    pass