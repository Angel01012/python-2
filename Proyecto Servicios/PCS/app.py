from flask import Flask
from database import db
from config import BasicConfig
from flask_migrate import Migrate
import logging
from routes.Producto.producto import appproducto
from routes.Comida.comida import appcomida
from routes.Cliente.cliente import appcliente

app = Flask(__name__)
app.register_blueprint(appproducto)
app.register_blueprint(appcomida)
app.register_blueprint(appcliente)
app.config.from_object(BasicConfig)
db.init_app(app)
migrate = Migrate()
migrate.init_app(app,db)

logging.basicConfig(level=logging.DEBUG,filename="debug.log")
