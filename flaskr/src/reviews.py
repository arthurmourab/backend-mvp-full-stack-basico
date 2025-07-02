from flask import request, session
from flask_restx import Namespace, Resource, fields
from flaskr.models import db, Review, WatchedMovie
from sqlalchemy.exc import IntegrityError

api = Namespace('reviews', description='Avaliações de filmes')

review_model = api.model('Review', {
    'movie_id': fields.Integer(required=True),
    'title': fields.String(required=True),
    'content': fields.String(required=True),
    'rating': fields.Float(required=True, description='Nota de 0 a 10')
})


@api.route('/')
class ReviewResource(Resource):
    @api.expect(review_model)
    @api.response(201, 'Avaliação salva')
    @api.response(400, 'Erro na avaliação')
    def post(self):
        """Cria uma avaliação de um filme"""
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Usuário não autenticado'}, 400

        data = request.get_json()
        movie_id = data.get('movie_id')
        rating = data.get('rating')

        if rating is None or not (0 <= rating <= 10):
            return {'error': 'Nota deve estar entre 0 e 10'}, 400

        # Verifica se já assistiu
        existing = WatchedMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if not existing:
            return {'message': 'Filme ainda não assistido. Você precisa assistir o filme para poder avaliar'}, 200

        # Verifica se já avaliou
        existingReview = Review.query.filter_by(author_id=user_id, movie_id=movie_id).first()
        if existingReview:
            return {'message': 'Filme já avaliado. Você não pode avaliar o mesmo filme mais de uma vez'}, 200

        # Cria nova
        new_review = Review(
            title=data.get('title'),
            content=data.get('content'),
            rating=rating,
            movie_id=movie_id,
            author_id=user_id
        )
        db.session.add(new_review)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Erro ao salvar avaliação'}, 400

        return {'message': 'Avaliação salva com sucesso'}, 201

