DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS watched_movies;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT UNIQUE NOT NULL,
    name      TEXT        NOT NULL,
    last_name TEXT        NOT NULL,
    email     TEXT UNIQUE NOT NULL,
    password  TEXT        NOT NULL
);

CREATE TABLE movies
(
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT    NOT NULL,
    genre TEXT    NOT NULL,
    year  INTEGER NOT NULL,
    cover TEXT    NOT NULL
);

CREATE TABLE watched_movies
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    date     TEXT    NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (movie_id) REFERENCES movies (id),
    UNIQUE (user_id, movie_id)
);


CREATE TABLE reviews
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    content   TEXT    NOT NULL,
    movie_id  INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    rating    REAL    NOT NULL CHECK (rating >= 0 AND rating <= 10),
    FOREIGN KEY (author_id) REFERENCES users (id),
    FOREIGN KEY (movie_id) REFERENCES movies (id),
    UNIQUE (author_id, movie_id)
);

