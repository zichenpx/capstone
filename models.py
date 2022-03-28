import os
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
# --------------------------------------------------
# App Config.
# --------------------------------------------------
load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
database_name = DB_NAME
database_path = "postgres://{}:{}@{}:{}/{}".format(DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

# database_name = "capstone"
# database_path = "postgres://{}:{}@{}/{}".format("postgres", "password", "localhost:5432", database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()
# --------------------------------------------------
# 關聯表單 - Movie(One) 對 Actor(Many)
# 必須放在 Model 前面，不然會有 error - point
# --------------------------------------------------
actor_in_movie = db.Table(
  "actor_in_movie",
  db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
  db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True)
)
# --------------------------------------------------
# Model - Movie
# --------------------------------------------------
class Movie(db.Model):
  __tablename__ = "movies"

  id = Column(Integer, primary_key=True)
  title = Column(String(256), nullable=False)
  release_year = Column(Integer, nullable=False)
  duration = Column(Integer, nullable=False)
  cast = db.relationship("Actor", secondary=actor_in_movie, backref=db.backref("movies", lazy=True))
  imdb_rating = Column(Float, nullable=False)

  def __init__(self, title, release_year, duration, imdb_rating):
    self.title = title
    self.release_year = release_year
    self.duration = duration
    self.imdb_rating = imdb_rating

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def breif(self):
    return {
      "id": self.id,
      "title": self.title,
      "release_year": self.release_year,
      "imdb_rating": self.imdb_rating
    }

  def full_info(self):
    return {
      "id": self.id,
      "title": self.title,
      "duration": self.duration,
      "release_year": self.release_year,
      "cast": [actor.name for actor in self.cast],
      "imdb_rating": self.imdb_rating
    }

  def __repr__(self):
    return "<Movie {} {} {} {} />".format(self.title, self.release_year, self.imdb_rating, self.duration)

# --------------------------------------------------
# Model - Actor
# --------------------------------------------------
class Actor(db.Model):
  __tablename__ = "actors"

  id = Column(Integer, primary_key=True)
  name = Column(String(256), nullable=False)
  date_of_birth = Column(Date, nullable=False)
  gender = Column(String, nullable=True)
  # Pending: 改 gender's datatype

  def __init__(self, name, date_of_birth, gender):
    self.name = name
    self.date_of_birth = date_of_birth
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def breif(self):
    return {
      "id": self.id,
      "name": self.name,
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

  #  def full_info(self):
  #   return {
  #     "id": self.id,
  #     "name": self.name,
  #     "date_of_birth": self.date_of_birth.strftime("%B %d, %Y"),
  #     "gender": self.gender,
  #     "movies": [movie.title for movie in self.movies]
  #   }
  # strftime() for date, datetime, time. 注意格式
  # strptime() for datetime only

  def __repr__(self):
    return "<Actor {} {} {} />".format(self.name, self.date_of_birth, self.gender)

