from flask import Blueprint,make_response,render_template,url_for,current_app
from models import User,Servicio,Tipo_Servicio,Tecnico,Cliente
from sqlalchemy.orm import aliased
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from app import db

apppdf = Blueprint('apppdf',__name__,template_folder="templates")


@apppdf.route('/generatePdf/<int:id>')
def generate_pdf(id):
    servicioobtenido = Servicio.query.get_or_404(id)
    cliente = Cliente.query.get_or_404(servicioobtenido.cliente_id)
    doc = SimpleDocTemplate(f"service{id}.pdf", pagesize=letter)
    #logo_path = '../../static/pacman.png'
    #logo = Image(logo_path, width=100, height=100)
    #elements = [logo]

    logo_path = current_app.root_path + url_for('static', filename='images/pacman.png')
    logo = Image(logo_path,width=450,height=150)
    elements = [logo]

    TecnicoAlias = aliased(Tecnico)
    Tipo_ServicioAlias = aliased(Tipo_Servicio)

    serviciocompuesto = (
    db.session.query(Servicio, Tipo_Servicio, Tecnico)
    .join(Tipo_ServicioAlias, Servicio.tipo_servicio_id == Tipo_ServicioAlias.id)
    .join(TecnicoAlias, Servicio.tecnico_id == TecnicoAlias.id)
    .filter(
        Servicio.tecnico_id == Tecnico.id,
        Servicio.tipo_servicio_id == Tipo_Servicio.id
    )
    .all()
    )
    #print(serviciocompuesto)
    numservicio = 0
    suma = 0
    listaServicios=[["FECHA","CONCEPTO","COSTO","STATUS","TECNICO","TIPO DE SERVICIO"]]
    for servicio,tipo_servicio,tecnico in serviciocompuesto:
        if servicio.cliente_id == servicioobtenido.cliente_id:
            nuevoservicio = Servicio(id=servicio.id,concepto=servicio.concepto,costo=servicio.costo,status=servicio.status,tecnico_id=tecnico.nombre,tipo_servicio_id=tipo_servicio.nombre,cliente_id=cliente.nombre,registered_input=servicio.registered_input)
            numservicio= numservicio + 1
            suma = suma + float(servicio.costo)
            listaServicios.append([nuevoservicio.registered_input,nuevoservicio.concepto,nuevoservicio.costo,nuevoservicio.status,nuevoservicio.tecnico_id,nuevoservicio.tipo_servicio_id])
            #print(nuevoservicio)
    print(listaServicios)
    table = Table(listaServicios)

    style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 16),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    table.setStyle(style)
    # Add the table to the PDF document

    text = f"Lista de servicios del {cliente.nombre}"

    # Create a paragraph object
    style = getSampleStyleSheet()["Normal"]
    style.alignment = TA_CENTER 
    paragraph = Paragraph(text, style)
    elements.append(paragraph)
    elements.append(table)
    text2 = f"el cliente {cliente.nombre} ha pagado un total de: ${suma} por un numero total de servicios de: {numservicio}"
    paragrafia = Paragraph(text2,style=getSampleStyleSheet()["Normal"])
    elements.append(paragrafia)
    
    doc.build(elements)

    # Create a response with the PDF file
    response = make_response(open(f"service{id}.pdf", "rb").read())

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=service{id}.pdf'
    return response

