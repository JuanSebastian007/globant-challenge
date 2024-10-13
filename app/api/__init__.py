from flask import Blueprint

# Crear un Blueprint para las rutas de la API
api_bp = Blueprint('api', __name__)

# Importar las rutas para que se registren
from app.api import routes
