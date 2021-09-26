import os
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# --------------------------------------------------
# App Config.
# --------------------------------------------------
database_path = os.environ.get('DATABASE_URL')
if not database_path:
  database_name = "capstone"
  database_path = "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()

# --------------------------------------------------
# Model
# --------------------------------------------------
actor_in_movie = db.Table(
    'actor_in_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)

class Movie(db.Model):
  __tablename__ = "movies"

  id = Column(Integer, primary_key=True)
  title = Column(String(256), nullable=False)
  release_year = Column(Integer, nullable=False)
  duration = Column(Integer, nullable=False)
  imdb_rating = Column(Float, nullable=False)
  cast = db.relationship('Actor', secondary=actor_in_movie, backref=db.backref('movies', lazy=True))

  def __init__(self, title, release_year, duration, imdb_rating):
    self.title = title
    self.release_year = release_year
    self.duration = duration
    self.imdb_rating = imdb_rating

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def short(self):
    return {
      "id": self.id,
      "title": self.title,
      "release_year": self.release_year
    }

  def long(self):
    return {
      "title": self.title,
      "duration": self.duration,
      "release_year": self.release_year,
      "imdb_rating": self.imdb_rating
    }

  def full_info(self):
    return {
      "id": self.id,
      "title": self.title,
      "duration": self.duration,
      "release_year": self.release_year,
      "imdb_rating": self.imdb_rating,
      "cast": [actor.name for actor in self.cast]
    }

  def __repr__(self):
    return "<Movie {} {} {} {} />".format(self.title, self.release_year, self.imdb_rating, self.duration)


class Actor(db.Model):
  __tablename__ = "actors"

  id = Column(Integer, primary_key=True)
  name = Column(String(256), nullable=False)
  date_of_birth = Column(Date, nullable=False)
  gender = Column(String, nullable=True)

  def __init__(self, name, date_of_birth, gender):
    self.name = name
    self.date_of_birth = date_of_birth
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def short(self):
    return {
      "id": self.id,
      "name": self.name
    }

  def long(self):
    return {
      "name": self.name,
      "date_of_birth": self.date_of_birth.strftime("%B %d, %Y"),
      "gender": self.gender
    }

  def full_info(self):
    return {
      "id": self.id,
      "name": self.name,
      "date_of_birth": self.date_of_birth.strftime("%B %d, %Y"),
      "gender": self.gender,
      "movies": [movie.title for movie in self.movies]
    }

  def __repr__(self):
    return "<Movie {} {} {} />".format(self.name, self.date_of_birth, self.gender)