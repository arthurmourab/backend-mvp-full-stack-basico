from flask.cli import with_appcontext
import click
from flaskr.models import db, User, Movie, WatchedMovie, Review
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

@click.command('seed-db')
@with_appcontext
def seed_db():
    """Popula o banco com usuários, filmes, visualizações e reviews"""
    db.drop_all()
    db.create_all()

    # Criar usuários
    users = [
        User(username='alice123', name='Alice', last_name='Silva', email='alice@example.com', password=generate_password_hash('senha1')),
        User(username='bruno_dev', name='Bruno', last_name='Costa', email='bruno@example.com', password=generate_password_hash('senha2')),
        User(username='carol_art', name='Carol', last_name='Dias', email='carol@example.com', password=generate_password_hash('senha3')),
        User(username='daniel77', name='Daniel', last_name='Oliveira', email='daniel@example.com', password=generate_password_hash('senha4')),
        User(username='erika_x', name='Erika', last_name='Santos', email='erika@example.com', password=generate_password_hash('senha5')),
    ]
    db.session.add_all(users)
    db.session.commit()

    # Criar filmes
    movies = [
        Movie(name='Matrix', genre='Ficção Científica', year=1999, cover='matrix.jpg'),
        Movie(name='Titanic', genre='Romance', year=1997, cover='titanic.jpg'),
        Movie(name='O Senhor dos Anéis', genre='Fantasia', year=2001, cover='lotr.jpg'),
        Movie(name='Interestelar', genre='Ficção Científica', year=2014, cover='interestelar.jpg'),
        Movie(name='Clube da Luta', genre='Drama', year=1999, cover='clubedaluta.jpg'),
        Movie(name='A Origem', genre='Ação', year=2010, cover='aorigem.jpg'),
        Movie(name='Corra!', genre='Suspense', year=2017, cover='corra.jpg'),
        Movie(name='Toy Story', genre='Animação', year=1995, cover='toystory.jpg'),
        Movie(name='Pantera Negra', genre='Ação', year=2018, cover='panteranegra.jpg'),
        Movie(name='Parasita', genre='Drama', year=2019, cover='parasita.jpg'),
    ]
    db.session.add_all(movies)
    db.session.commit()

    # Criar assistidos + reviews
    for user in users:
        sampled_movies = random.sample(movies, 3)
        for movie in sampled_movies:
            watch = WatchedMovie(user_id=user.id, movie_id=movie.id, date=datetime.now().isoformat())
            review = Review(
                title=f'Review de {movie.name}',
                content=f'Gostei do filme {movie.name}!',
                rating=round(random.uniform(7.5, 10.0), 1),
                author_id=user.id,
                movie_id=movie.id
            )
            db.session.add(watch)
            db.session.add(review)

    db.session.commit()
    click.echo('Banco populado com sucesso!')
