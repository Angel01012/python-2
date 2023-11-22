from flask import Flask,render_template
from database import db
from config import BasicConfig
from flask_migrate import Migrate
from flask_cors import CORS
from encriptador import bcrypt
#from routes.jugador.jugador import appjugador
import logging

app = Flask(__name__)
#app.register_blueprint(appjugador)
app.config.from_object(BasicConfig)
CORS(app)
db.init_app(app)
migrate = Migrate()
migrate.init_app(app,db)
logging.basicConfig(level=logging.DEBUG,filename="debug.log")