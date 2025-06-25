from flask_restx import Namespace, Resource, fields
from flaskr.models import db, Movie, WatchedMovie
from sqlalchemy import func

api = Namespace('movies', description='Operações relacionadas a filmes')

# Modelo para resposta resumida (lista)
movie_summary = api.model('MovieSummary', {
    'id': fields.Integer,
    'name': fields.String,
    'genre': fields.String,
    'year': fields.Integer,
    'cover': fields.String,
    'views': fields.Integer(description="Quantidade de vezes que foi assistido")
})

# Modelo para resposta detalhada (um filme)
movie_detail = api.model('MovieDetail', {
    'id': fields.Integer,
    'name': fields.String,
    'genre': fields.String,
    'year': fields.Integer,
    'cover': fields.String,
    'views': fields.Integer,
    'average_rating': fields.Float
})


@api.route('')
class MovieList(Resource):
    @api.response(200, 'Lista de filmes retornada com sucesso')
    @api.marshal_list_with(movie_summary)
    def get(self):
        """Lista todos os filmes ordenados por número de visualizações"""
        movies = (
            db.session.query(
                Movie,
                func.count(WatchedMovie.id).label('views')
            )
            .outerjoin(WatchedMovie, WatchedMovie.movie_id == Movie.id)
            .group_by(Movie.id)
            .order_by(func.count(WatchedMovie.id).desc())
            .all()
        )

        # Transformar a resposta
        result = []
        for movie, views in movies:
            result.append({
                'id': movie.id,
                'name': movie.name,
                'genre': movie.genre,
                'year': movie.year,
                'cover': movie.cover,
                'views': views
            })
        return result


from flaskr.models import Movie, WatchedMovie, Review
from sqlalchemy import func

@api.route('/<int:id>')
@api.param('id', 'ID do filme')
class MovieDetail(Resource):
    @api.response(200, 'Detalhes do filme retornados com sucesso')
    @api.response(404, 'Filme não encontrado')
    @api.marshal_with(movie_detail)
    def get(self, id):
        """Obtém detalhes de um filme específico"""
        movie = Movie.query.get(id)
        if not movie:
            api.abort(404, 'Filme não encontrado')

        # Contar visualizações
        views = WatchedMovie.query.filter_by(movie_id=id).count()

        # Calcular média de notas
        avg_rating = db.session.query(func.avg(Review.rating)).filter_by(movie_id=id).scalar()
        avg_rating = round(avg_rating, 2) if avg_rating is not None else None

        return {
            'id': movie.id,
            'name': movie.name,
            'genre': movie.genre,
            'year': movie.year,
            'cover': movie.cover,
            'views': views,
            'average_rating': avg_rating
        }

