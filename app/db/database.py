from flask_sqlalchemy import SQLAlchemy

# Inicializar la instancia de SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Inicializa la base de datos con la app Flask"""
    db.init_app(app)
