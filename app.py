import os
from flask import Flask, request, abort, jsonify
from sqlalchemy import Date
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import null
from models import setup_db, Movie, Actor, db
import time
from datetime import datetime
# from auth import AuthError, requires_auth

# --------------------------------------------------
# App Config.
# --------------------------------------------------
def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS")
    return response

# --------------------------------------------------
# Routes.
# --------------------------------------------------
  @app.route("/")
  def index():
    result = {
      "success": True,
      "state": "Running!!",
      "health": "Good!!",
      "message": "Welcome to My Full Stack Capstone Project"
    }
    return jsonify(result), 200

  @app.route("/movies")
  # @requires_auth("get:movies")
  def get_movies():
    query_movies = Movie.query.order_by(Movie.id).all()
    movies = [movie.breif() for movie in query_movies]
    result = {
      "success": True,
      "movies": movies
    }
    return jsonify(result), 200

  @app.route("/movies/<int:movie_id>")
  # @requires_auth("get:movies-detail")
  def get_movie_by_id(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    result = {
      "success": True,
      "movie": movie.full_info()
    }
    return jsonify(result), 200

  @app.route("/movies", methods=["POST"])
  # @requires_auth("post:movie")
  def create_movie():
    data = request.get_json()
    
    if "title" not in data \
        or "release_year" not in data \
        or "duration" not in data \
        or "cast" not in data \
        or "imdb_rating" not in data:
      abort(422)

    if data["title"] == "" \
        or data["release_year"] <= 0 \
        or data["release_year"] == "" \
        or data["duration"] <= 0 \
        or len(data["cast"]) == 0 \
        or data["imdb_rating"] < 0 \
        or data["imdb_rating"] >10:
      abort(422)
      # TypeError: '<=' not supported between instances of 'str' and 'int'

    try:

      cast = Actor.query.filter(Actor.name.in_(data["cast"])).all()

      new_movie = Movie(
        data["title"],
        data["release_year"],
        data["duration"],
        # cast,
        data["imdb_rating"]
      )
      new_movie.cast = cast

    except Exception:
      db.session.rollback()
      abort(500)

    finally:
      new_movie.insert()
      result = {
        "success": True,
        "movie": [new_movie.full_info()],
        "total_movies": len(Movie.query.all())
      }
      return jsonify(result), 201

  @app.route("/movies/<int:movie_id>", methods=["PATCH"])
  # @requires_auth("patch:movie")
  def update_movies(movie_id):
    data = request.get_json()
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    try: 
      if "title" in data:
        if data["title"] == "":
          raise ValueError
        movie.title = data["title"]

      if "release_year" in data:
        if data["release_year"] <= 0:
          raise ValueError
        movie.release_year = data["release_year"]

      if "duration" in data:
        if data["duration"] <= 0:
          raise ValueError
        movie.duration = data["duration"]

      if "cast" in data:
        if len(data["cast"]) == 0:
          raise ValueError
        cast = Actor.query.filter(Actor.name.in_(data["cast"])).all()
        # if len(data["cast"]) > len(actors):
        movie.cast = cast
        # else:
        #   raise ValueError

      if "imdb_rating" in data:
        if data["imdb_rating"] < 0 or data["imdb_rating"] > 10:
          raise ValueError
        movie.imdb_rating = data["imdb_rating"]

    except (TypeError, ValueError, KeyError):
      db.session.rollback()
      abort(422)

    except Exception:
      db.session.rollback()
      abort(500)

    finally:
      movie.update()
      result = {
        "success": True,
        "movie_info": movie.full_info()
      }
      return jsonify(result), 200

  @app.route("/movies/<int:movie_id>", methods=["DELETE"])
  # @requires_auth("delete:movie")
  def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    
    try:
      movie.delete()

    except Exception:
      db.session.rollback()
      abort(500)

    finally:
      result = {
        "success": True,
        "deleted": movie_id,
        "total_movies": len(Movie.query.all())
      }
      return jsonify(result), 200

  @app.route("/actors")
  # @requires_auth("get:actors")
  def get_actors():
    query_actors = Actor.query.order_by(Actor.id).all()
    actors = [actor.breif() for actor in query_actors]
    result = {
      "success": True,
      "actors": actors
    }
    return jsonify(result), 200

  @app.route("/actors/<int:actor_id>")
  # @requires_auth("get:actor-detail")
  def get_actor_by_id(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    result = {
      "success": True,
      "actor": actor.full_info()
    }
    return jsonify(result), 200

  @app.route("/actors", methods=["POST"])
 # @requires_auth("post:actor")
  def create_actor():
    data = request.get_json()
    
    if "name" not in data \
        or "date_of_birth" not in data \
        or "gender" not in data:
      abort(422)

    if data["name"] == "" \
        or data["date_of_birth"] == "" \
        or data["gender"] == "":
      abort(422)

    try:
      name = data["name"]
      date_of_birth = data["date_of_birth"]
      gender = data["gender"]

      new_actor = Actor(name, date_of_birth, gender)
      new_actor.insert()

    except Exception:
      db.session.rollback()
      abort(500)

    finally:
      result = {
        "success": True,
        "actor": [new_actor.full_info()],
        "total_actors": len(Actor.query.all())
      }
      return jsonify(result), 201

  @app.route("/actors/<int:actor_id>", methods=["PATCH"])
  # @requires_auth("patch:actor")
  def update_actor(actor_id):
    data = request.get_json()
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    try:  
      if "name" in data:
        if data["name"] == "":
          raise ValueError
        actor.name = data["name"]

      if "date_of_birth" in data:
        if data["date_of_birth"] == "":
          raise ValueError
        actor.date_of_birth = data["date_of_birth"]

      if "gender" in data:
        if data["gender"] == "":
          raise ValueError
        actor.gender = data["gender"]
      

    except (TypeError, ValueError, KeyError):
      db.session.rollback()
      abort(422)

    except Exception:
      db.session.rollback()
      abort(500)
     
    finally:
      actor.update()
      result = {
        "success": True,
        "updated": actor_id,
        "actor_info": actor.full_info()
      }
      return jsonify(result), 200
    

  @app.route("/actors/<int:actor_id>", methods=["DELETE"])
  # @requires_auth("delete:actor")
  def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    
    try:
      actor.delete()

    except Exception:
      db.session.rollback()
      abort(500)
    
    finally:
      result = {
        "success": True,
        "deleted": actor_id,
        "total_actors": len(Actor.query.all())
      }
      return jsonify(result), 200


# --------------------------------------------------
# Error Handling
# --------------------------------------------------
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

  @app.errorhandler(404)
  def resource_not_found(error):
      return (
          jsonify({"success": False, "error": 404, "message": "resource not found"}),
          404,
      )

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return (
      jsonify({"success": False, "error": 500, "message": "internal server error"}),
      500,
    )

  # @app.errorhandler(AuthError)
  # def handle_auth_error(exception):
  #   response = jsonify(exception.error)
  #   response.status_code = exception.status_code
  #   return response  

  return app

APP = create_app()

if __name__ == "__main__":
  APP.run(host="0.0.0.0", port=8080, debug=True)