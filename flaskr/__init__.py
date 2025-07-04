import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Criação global do SQLAlchemy
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Configurações da aplicação
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(
            os.path.join(app.instance_path, 'flaskr.sqlite')
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    # Garante que a pasta instance/ existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa o banco de dados
    db.init_app(app)

    # Importar namespaces, blueprints e rotas **aqui dentro**, após criar app e inicializar db
    from flaskr.src.auth import api as auth_api
    from flaskr.src.movies import api as movies_api
    from flaskr.src.reviews import api as reviews_api
    from flaskr.src.watched import api as watched_api

    from flask_restx import Api
    from .seed import seed_db

    # Inicializa o Swagger (Flask-RESTX)
    api = Api(
        app,
        title="MVP Backend API",
        version="1.0",
        description="Documentação da API REST",
        doc="/swagger"  # Documentação disponível em /swagger
    )

    # Registra os namespaces (rotas organizadas)
    api.add_namespace(auth_api, path='/auth')
    api.add_namespace(movies_api, path='/movies')
    api.add_namespace(reviews_api, path='/reviews')
    api.add_namespace(watched_api, path='/watched')

    CORS(app, supports_credentials=True)

    app.cli.add_command(seed_db)
    return app
