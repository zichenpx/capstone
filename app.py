import os
from flask import Flask, request, abort, jsonify
from sqlalchemy import Date
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
# from auth import AuthError, requires_auth

# --------------------------------------------------
# App Config.
# --------------------------------------------------

def create_app(test_config=None):
  # create and configure the app
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
  @app.route('/')
  def index():
    return jsonify({
      "success": True,
      "state": "Running!!",
      "health": "Good!!",
      "message": "Welcome to My Full Stack Capstone Project"
    }), 200

  @app.route('/movies')
  # @requires_auth('get:movies')
  def get_movies():
    query_movies = Movie.query.order_by(Movie.id).all()
    movies = [movie.short() for movie in query_movies]

    return jsonify({
      "success": True,
      "movies": movies
    }), 200

  @app.route('/movies/<int:movie_id>')
  # @requires_auth('get:movies-detail')
  def get_movie_by_id(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    return jsonify({
      "success": True,
      "movie": movie.full_info()
    }), 200

  @app.route('/movies', methods=['POST'])
  # @requires_auth('post:movie')
  def create_movie():
    request_body = request.get_json()
    
    if "title" not in request_body \
        or "release_year" not in request_body \
        or "duration" not in request_body \
        or "imdb_rating" not in request_body \
        or "cast" not in request_body:
      abort(422)

    if request_body["title"] == "" \
        or request_body["release_year"] <= 0 \
        or request_body["duration"] <= 0 \
        or request_body["imdb_rating"] < 0 \
        or request_body["imdb_rating"] >10 \
        or len(request_body["cast"]) == 0:
      abort(422)

    try:
      new_movie = Movie(
        request_body["title"],
        request_body["release_year"],
        request_body["duration"],
        request_body["imdb_rating"],
        request_body["cast"]
      )
      
    except Exception:
      db.session.rollback()
      abort(500)

    finally:
      return jsonify({
        "success": True,
        "created_movie_id": new_movie.id,
        "movie": [new_movie.full_info()],
        "total_movies": len(Movie.query.all())
      }), 201

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  # @requires_auth("patch:movie")
  def update_movies(movie_id):
    request_body = request.get_json()
    print(request_body)
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    try:  
      if "title" in request_body:
        if request_body["title"] == "":
          raise ValueError
        movie.title = request_body["title"]

      if "release_year" in request_body:
        if request_body["release_year"] <= 0:
          raise ValueError
        movie.release_year = request_body["release_year"]

      if "duration" in request_body:
        if request_body["duration"] <= 0:
          raise ValueError
        movie.duration = request_body["duration"]

      if "imdb_rating" in request_body:
        if request_body["imdb_rating"] < 0 or request_body["imdb_rating"] > 10:
          raise ValueError
        movie.imdb_rating = request_body["imdb_rating"]

      if "cast" in request_body:
        if len(request_body["cast"]) == 0:
          raise ValueError
        actors = Actor.query.filter(Actor.name.in_(request_body["cast"])).all()
        if len(request_body["cast"]) == len(actors):
          movie.cast = actors
        else:
          raise ValueError

      movie.update()

    except (TypeError, ValueError, KeyError):
      db.session.rollback()
      abort(422)

    except Exception:
      db.session.rollback()
      abort(500)

    finally:
      return jsonify({
        "success": True,
        "movie_info": movie.full_info()
      }), 200

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  # @requires_auth('delete:movie')
  def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    
    try:
      movie.delete()

      return jsonify({
        "success": True,
        "deleted": movie_id,
        "total_movies": len(Movie.query.all())
      })


    except Exception:
      db.session.rollback()
      abort(500)

  @app.route('/actors')
  # @requires_auth('get:actors')
  def get_actors():
    query_actors = Actor.query.order_by(Actor.id).all()
    actors = [actor.short() for actor in query_actors]

    return jsonify({
      "success": True,
      "actors": actors
    }), 200

  @app.route('/actors/<int:actor_id>')
  # @requires_auth('get:actor-detail')
  def get_actor_by_id(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    return jsonify({
      "success": True,
      "actor": actor.full_info()
    }), 200

  @app.route('/actors', methods=['POST'])
 # @requires_auth('post:actor')
  def create_actor():
    request_body = request.get_json()
    print(request_body)
    
    if "name" not in request_body \
        or "date_of_birth" not in request_body \
        or "gender" not in request_body:
      abort(422)

    if request_body["name"] == "" \
        or request_body["date_of_birth"] == "" \
        or request_body["gender"] == "":
      abort(422)

    try:
      name = request_body["name"]
      date_of_birth = str(request_body["date_of_birth"])
      gender = request_body["gender"]

      new_actor = Actor(name, date_of_birth, gender)

    except Exception:
      db.session.rollback()
      abort(500)

    finally:
      return jsonify({
        "success": True,
        "created_actor_id": new_actor.id,
        "actor": [new_actor.full_info()],
        "total_actors": len(Actor.query.all())
      }), 201

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  # @requires_auth("patch:actor")
  def update_actor(actor_id):
    request_body = request.get_json()
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    try:  
      if "name" in request_body:
        if request_body["name"] == "":
          raise ValueError
        actor.name = request_body["name"]

      if "date_of_birth" in request_body:
        if request_body["date_of_birth"] == "":
          raise ValueError
        actor.date_of_birth = request_body["date_of_birth"]

      if "gender" in request_body:
        if request_body["gender"] == "":
          raise ValueError
        actor.gender = request_body["gender"]

      actor.update()

    except (TypeError, ValueError, KeyError):
      db.session.rollback()
      abort(422)

    except Exception:
      db.session.rollback()
      abort(500)
     
    finally:
      return jsonify({
        "success": True,
        "actor_info": actor.full_info()
      }), 200
    

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  # @requires_auth('delete:actor')
  def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    
    try:
      actor.delete()

      return jsonify({
        "success": True,
        "deleted": actor_id,
        "total_actors": len(Actor.query.all())
      })

    except Exception:
      db.session.rollback()
      abort(500)


# # --------------------------------------------------
# # Error Handling
# # --------------------------------------------------
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

if __name__ == '__main__':
    
    APP.run(host='0.0.0.0', port=8080, debug=True)