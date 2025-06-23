from flask import request, jsonify, session
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models import User
from flaskr import db

api = Namespace('auth', description='Operações de autenticação')

# Modelo de usuário para documentação de entrada
user_model = api.model('User', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'name': fields.String(required=True, description='Primeiro nome'),
    'last_name': fields.String(required=True, description='Último nome'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Senha')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Senha')
})

@api.route('/register')
class Register(Resource):
    @api.expect(user_model)
    @api.response(201, 'Usuário registrado com sucesso')
    @api.response(400, 'Dados inválidos ou usuário já existe')
    def post(self):
        """Registra um novo usuário"""
        data = request.get_json()
        username = data.get('username')
        name = data.get('name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        if not username or not name or not last_name or not email or not password:
            return {'error': 'Todos os campos são obrigatórios.'}, 400

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {'error': 'Usuário com esse username ou email já existe.'}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            name=name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Usuário registrado com sucesso'}, 201


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login bem-sucedido')
    @api.response(401, 'Credenciais inválidas')
    def post(self):
        """Realiza login do usuário"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return {'error': 'Credenciais inválidas'}, 401

        session.clear()
        session['user_id'] = user.id

        return {'message': 'Login bem-sucedido', 'user_id': user.id}, 200
