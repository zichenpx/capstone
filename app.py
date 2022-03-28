import os
from flask import Flask, request, abort, jsonify, render_template
from sqlalchemy import Date
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import null
from models import setup_db, Movie, Actor, db
import time
from datetime import datetime
from auth import AuthError, requires_auth

# --------------------------------------------------
# App Config.
# --------------------------------------------------
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
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
    @requires_auth("get:movies")
    def get_movies(payload):
        query_movies = Movie.query.order_by(Movie.id).all()
        movies = [movie.breif() for movie in query_movies]
        result = {
            "success": True,
            "movies": movies
        }
        return jsonify(result), 200

    @app.route("/movies/<int:movie_id>")
    @requires_auth("get:movies-detail")
    def get_movie_by_id(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        result = {
            "success": True,
            "movie": movie.full_info()
        }
        return jsonify(result), 200

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movie")
    def create_movie(payload):
        error = False
        data = request.get_json()

        # ISSUE: TypeError: '<=' not supported between instances of 'str' and 'int'
        # 因為如果 input 為 "" 則會有問題，所以依資料型態分開判斷處理
        if "title" not in data \
              or "release_year" not in data \
              or "duration" not in data \
              or "cast" not in data \
              or "imdb_rating" not in data \
              or data["title"] == "" \
              or data["release_year"] == "" \
              or data["duration"] == "" \
              or len(data["cast"]) == 0 \
              or data["imdb_rating"] == "":
            abort(422)

        if data["release_year"] <= 0 \
              or data["duration"] <= 0 \
              or data["imdb_rating"] < 0 \
              or data["imdb_rating"] >10:
            abort(422)

        try:
          cast = Actor.query.filter(Actor.name.in_(data["cast"])).all()
          new_movie = Movie(
              data["title"],
              data["release_year"],
              data["duration"],
              # cast,
              data["imdb_rating"]
          )
          if len(data["cast"]) == len(cast):
              new_movie.cast = cast
          elif len(data["cast"]) > len(cast):
              error = True
          else:
              raise Exception
          new_movie.cast = cast

        except Exception:
            db.session.rollback()
            abort(500)

        finally:
            if error == True:
                return jsonify({
                    "message": "Please check cast are all in the database."
                })

            new_movie.insert()
            result = {
                "success": True,
                "movie": [new_movie.full_info()],
                "total_movies": len(Movie.query.all())
            }
            return jsonify(result), 201

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth("patch:movie")
    def update_movies(payload, movie_id):
        error = False
        typing_error = False
        unexpected_error = False
        data = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        if "title" in data:
            if data["title"] == "":
                typing_error = True
            movie.title = data["title"]

        if "release_year" in data:
            if data["release_year"] == "":
                typing_error = True
            else:
                if data["release_year"] <= 0:
                  typing_error = True
                movie.release_year = data["release_year"]

        if "duration" in data:
            if data["duration"] == "":
                typing_error = True
            else:
                if data["duration"] <= 0:
                   typing_error = True
                movie.duration = data["duration"]

        if "cast" in data:
            if len(data["cast"]) == 0:
                    typing_error = True
            cast = Actor.query.filter(Actor.name.in_(data["cast"])).all()
            if len(data["cast"]) == len(cast):
              movie.cast = cast
            elif len(data["cast"]) > len(cast):
              error = True
            else:
                unexpected_error = True
            
        if "imdb_rating" in data:
            if data["imdb_rating"] == "":
                typing_error = True
            else:
                if data["imdb_rating"] < 0 or data["imdb_rating"] > 10:
                  typing_error = True
                movie.imdb_rating = data["imdb_rating"]

        if error == True:
            # return ("Please check cast are all in the database.")
            return jsonify({
                "message": "Please check cast are all in the database."
            })

        if (typing_error):
            abort(422)

        if (unexpected_error):
            abort(500)

        movie.update()
        result = {
            "success": True,
            "movie_info": movie.full_info()
        }
        return jsonify(result), 200

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth("delete:movie")
    def delete_movie(payload, movie_id):
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
    @requires_auth("get:actors")
    def get_actors(payload):
        query_actors = Actor.query.order_by(Actor.id).all()
        actors = [actor.breif() for actor in query_actors]
        result = {
            "success": True,
            "actors": actors
        }
        return jsonify(result), 200

    @app.route("/actors/<int:actor_id>")
    @requires_auth("get:actors-detail")
    def get_actor_by_id(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        result = {
            "success": True,
            "actor": actor.full_info()
        }
        return jsonify(result), 200

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actor")
    def create_actor(payload):
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
            db.session.commit()
            result = {
              "success": True,
              "actor": [new_actor.full_info()],
              "total_actors": len(Actor.query.all())
            }
            return jsonify(result), 201

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth("patch:actor")
    def update_actor(payload, actor_id):
        error = False
        data = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        # print("1")
        if actor is None:
            # print("2")
            abort(404)

        if "name" in data:
            if data["name"] == "":
                error = True
                print(ValueError)
                # print("3")
            actor.name = data["name"]
            # print("33")

        if "date_of_birth" in data:
            if data["date_of_birth"] == "":
                error = True
                print(ValueError)
              # print("4")
            actor.date_of_birth = data["date_of_birth"]
            # print("44")

        if "gender" in data:
            if data["gender"] == "":
                error = True
                print(ValueError)
                # print("5")
            actor.gender = data["gender"]
            # print("55")

        if (error == True):
            # print("6")
            abort(422)
        
        # print("8")
        actor.update()
        # print("9")
        result = {
            "success": True,
            "updated": actor_id,
            "actor_info": actor.full_info()
        }
        return jsonify(result), 200
      

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth("delete:actor")
    def delete_actor(payload, actor_id):
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

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response  

    return app

app = create_app()

if __name__ == "__main__":
  app.run(host="https://tranquil-ridge-30288.herokuapp.com/")
#   app.run(host="0.0.0.0", port=8080, debug=True)