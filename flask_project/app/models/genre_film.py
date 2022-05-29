from app.database.flask_db import db

genre_film = db.Table("genre_film",
                      db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
                      db.Column("film_id", db.Integer, db.ForeignKey("film.id")))
