from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.db.database import init_db
from app.api import api_bp  # Importar el blueprint de la API

# Inicializar la instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Función de fábrica para crear una instancia de la aplicación Flask"""
    app = Flask(__name__)

    # Configuraciones de la app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://globant:globant@db/globant_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita el overhead de trackeo

    # Inicializar la base de datos
    init_db(app)

    # Registrar el blueprint de la API
    app.register_blueprint(api_bp, url_prefix='/api')  # Añade un prefijo de URL

    return app
