from flask import request, session
from flask_restx import Namespace, Resource, fields
from flaskr.models import db, WatchedMovie
from datetime import datetime

api = Namespace('watched', description='Filmes assistidos')

watched_model = api.model('Watched', {
    'movie_id': fields.Integer(required=True, description='ID do filme assistido')
})

@api.route('/')
class Watched(Resource):
    @api.expect(watched_model)
    @api.response(201, 'Filme marcado como assistido')
    @api.response(400, 'Requisição inválida')
    def post(self):
        """Marca um filme como assistido"""
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Usuário não autenticado'}, 400

        data = request.get_json()
        movie_id = data.get('movie_id')

        if not movie_id:
            return {'error': 'movie_id é obrigatório'}, 400

        # Verifica se já assistiu
        existing = WatchedMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing:
            return {'message': 'Filme já assitido. Você não pode marcar o mesmo filme mais de uma vez'}, 200

        watched = WatchedMovie(user_id=user_id, movie_id=movie_id, date=datetime.utcnow())
        db.session.add(watched)
        db.session.commit()
        return {'message': 'Filme marcado como assistido'}, 201
