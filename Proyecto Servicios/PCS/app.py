from flask import Flask,render_template,request
from database import db
from config import BasicConfig
from flask_migrate import Migrate
from flask_cors import CORS
from encriptador import bcrypt
from routes.user.user import appuser
from routes.tecnico.tecnico import apptecnico
from routes.cliente.cliente import appcliente
from routes.servicios.servicios import appservicio
from routes.pdf.pdf import apppdf
import logging




app = Flask(__name__)
app.register_blueprint(apppdf)
app.register_blueprint(appuser)
app.register_blueprint(apptecnico)
app.register_blueprint(appcliente)
app.register_blueprint(appservicio)
app.config.from_object(BasicConfig)
CORS(app)
db.init_app(app)
migrate = Migrate()
migrate.init_app(app,db)
logging.basicConfig(level=logging.DEBUG,filename="debug.log")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html')