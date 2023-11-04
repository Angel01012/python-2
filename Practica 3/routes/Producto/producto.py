from flask import Blueprint,request,redirect,render_template,url_for,jsonify
from models import Producto
from forms import ProductosForm
from app import db

appproducto = Blueprint('appproducto',__name__,template_folder="templates")

@appproducto.route('/')
def inicio():
    return render_template("index.html")
@appproducto.route('/listadoproducto')
def listadoproducto():
    productos = Producto.query.all()
    return render_template('listadoproducto.html',productos=productos)

@appproducto.route('/formularioproducto',methods=["GET","POST"])
def formularioproducto():
    producto = Producto()
    productoform = ProductosForm(obj=producto)
    if request.method == "POST":
        if productoform.validate_on_submit():
            productoform.populate_obj(producto)
            db.session.add(producto)
            db.session.commit()
            return redirect(url_for('appproducto.listadoproducto'))
    return render_template('formularioproducto.html',forma=productoform)

@appproducto.route('/editarproducto/<int:id>',methods=["GET","POST"])
def editarproducto(id):
    producto = Producto.query.get_or_404(id)
    productoform = ProductosForm(obj=producto)
    if request.method == "POST":
        if productoform.validate_on_submit():
            productoform.populate_obj(producto)
            db.session.commit()
            return redirect(url_for('appproducto.listadoproducto'))
    return render_template('editarproducto.html',forma=productoform)

@appproducto.route('/consultarproducto/<int:id>',methods=["GET","POST"])
def consultarproducto(id):
    producto = Producto.query.get_or_404(id)
    productos = [producto]
    #productoform = ProductosForm(obj=producto)
    
    return render_template('consultaproducto.html',productos=productos)

@appproducto.route('/eliminarproducto/<int:id>', methods=["POST","GET"])
def eliminarproducto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('appproducto.listadoproducto'))