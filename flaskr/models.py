from flaskr import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    watched_movies = db.relationship('WatchedMovie', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.String(300), nullable=False)

    watched_by = db.relationship('WatchedMovie', backref='movie', lazy=True)
    reviews = db.relationship('Review', backref='movie', lazy=True)

    def __repr__(self):
        return f'<Movie {self.name}>'

class WatchedMovie(db.Model):
    __tablename__ = 'watched_movies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    date = db.Column(db.String, nullable=False)

    # Garante que um usuário não assista o mesmo filme duas vezes
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),)

    def __repr__(self):
        return f'<WatchedMovie user_id={self.user_id}, movie_id={self.movie_id}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Restrição de nota entre 0 e 10
    __table_args__ = (
        db.CheckConstraint('rating >= 0 AND rating <= 10', name='valid_rating'),
        db.UniqueConstraint('author_id', 'movie_id', name='unique_review_per_user_movie')
    )

    def __repr__(self):
        return f'<Review {self.title} - movie_id={self.movie_id}>'
