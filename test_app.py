import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CapstoneTestCase(unittest.TestCase):

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "capstone"
    self.database_path = "postgres://{}:{}@{}/{}".format("postgres", "password", "localhost:5432", self.database_name)
    setup_db(self.app, self.database_path)

    self.new_movie = {
      "title": "Meow",
      "release_year": 2017,
      "duration": 100,
      "cast": ["Louis Koo"],
      "imdb_rating": 7.0
    }

    self.new_movie_invalid_data = {
      "title": "Meow",
      "release_year": "",
      "duration": 999,
      "cast": ["Louis Koo"],
      "imdb_rating": 7.0
    }

    self.new_movie_missing_data = {
       "title": "Meow",
      "release_year": 2017,
      "cast": ["Louis Koo"],
      "imdb_rating": 7.0
    }

    self.edited_movie = {
      "duration": 149,
      "cast": ["Julia Roberts", "Humphrey Bogart"]
    }

    self.edited_movie_invalid_data = {
      "duration": "",
      "gender": ""
    }

    self.new_actor = {
      "name": "Sarah Gray Rafferty",
      "date_of_birth": "December 6, 1972",
      "gender": "F"
    }

    self.new_actor_invalid_data = {
      "name": "Gabriel S. Macht",
      "date_of_birth": "",
      "gender": "M"
    }

    self.new_actor_missing_data = {
      "name": "Gabriel S. Macht",
      "date_of_birth": "January 22, 1972"
    }

    self.edited_actor = {
      "name": "Bradley Cooper",
      "date_of_birth": "January 5, 1975"
    }

    self.edited_actor_invalid_data = {
      "name": "",
      "imdb_rating": 12
    }

    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      self.db.create_all()
  
  def tearDown(self):
    """Executed after reach test"""
    pass

  # --------------------------------------------------
  # Test Index Running - Start
  # --------------------------------------------------
  def test_index_health(self):
    response = self.client().get("/")
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["success"], True)
    self.assertEqual(data["state"], "Running!!")
    self.assertEqual(data["health"], "Good!!")  
  # --------------------------------------------------
  # Test Index Running -End
  # --------------------------------------------------
  # --------------------------------------------------
  # Test Movies:GET, POST, PATCH, DELETE - Start
  # --------------------------------------------------
  # def test_get_movies(self):
  #   response = self.client().get("/movies")
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)
  #   self.assertTrue(len(data["movies"]))

  # def test_get_movie_by_id(self):
  #   response = self.client().get("/movies/1")
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)

  # def test_404_get_movie_id_not_exist(self):
  #   response = self.client().get("/movies/89852")
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 404)
  #   self.assertFalse(data["success"], True)    
      
  # def test_create_movie(self):
  #   response = self.client().post("/movies", json=self.new_movie)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 201)
  #   self.assertEqual(data["success"], True)

  # def test_422_create_movie_with_no_data(self):
  #   response = self.client().post("/movies", json={})
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True) 

# Start - ISSUE: flow logic issue. - 09272228
# TypeError: '<=' not supported between instances of 'str' and 'int'
  # def test_422_create_movie_with_invalid_data(self):
  #   response = self.client().post("/movies", json=self.new_movie_invalid_data)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True) 
# End - ISSUE: flow logic issue. - 09272228

  # def test_422_create_movie_with_missing_data(self):
  #   response = self.client().post("/movies", json=self.new_movie_missing_data)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True) 

  # def test_update_movie(self):
  #   r_id = 4
  #   response = self.client().patch("/movies/{}".format(r_id), json=self.edited_movie)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)

  # def test_404_update_movie_not_exist(self):
  #   r_id = 54982
  #   response = self.client().patch("/movies/{}".format(r_id), json=self.edited_movie)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 404)
  #   self.assertFalse(data["success"], True)

  # Start - ISSUE: ERROR, fail to stop input empty value. - 09272228
  # def test_422_update_movie_with_empty_data(self):
  #   r_id = 4
  #   response = self.client().patch("/movies/{}".format(r_id), json=self.edited_movie_invalid_data)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True)
  # End - ISSUE: ERROR, fail to stop input empty value. - 09272228

  # def test_delete_movie(self):
  #   r_id = 12
  #   response = self.client().delete("/movies/{}".format(r_id))
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)
  #   self.assertEqual(data["deleted"], r_id)

  # def test_404_delete_movie_not_exist(self):
  #   r_id = 868072
  #   response = self.client().delete("/movies/{}".format(r_id))
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 404)
  #   self.assertFalse(data["success"], True)
  # --------------------------------------------------
  # Test Movies:GET, POST, PATCH, DELETE - End
  # --------------------------------------------------
  # --------------------------------------------------
  # Test Actos:GET, POST, PATCH, DELETE - Start
  # --------------------------------------------------
  # def test_get_actors(self):
  #   response = self.client().get("/actors")
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)
  #   self.assertTrue(len(data["actors"]))

  # def test_get_actors_by_id(self):
  #   response = self.client().get("/actors/1")
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)

  # def test_404_get_actors_id_not_exist(self):
  #   response = self.client().get("/actors/8429031")
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 404)
  #   self.assertFalse(data["success"], True)  

  # def test_create_actor(self):
  #   response = self.client().post("/actors", json=self.new_actor)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 201)
  #   self.assertEqual(data["success"], True)

  # def test_422_create_actor_with_no_data(self):
  #   response = self.client().post("/actors", json={})
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True) 

  # def test_422_create_actor_with_invalid_data(self):
  #   response = self.client().post("/actors", json=self.new_actor_invalid_data)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True) 
  
  # def test_422_create_actor_with_missing_data(self):
  #   response = self.client().post("/actors", json=self.new_actor_missing_data)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True) 

  # def test_update_actor(self):
  #   r_id = 18
  #   response = self.client().patch("/actors/{}".format(r_id), json=self.edited_actor)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)
  #   self.assertEqual(data["updated"], r_id)

  # def test_404_update_actor_not_exist(self):
  #   r_id = 5106784
  #   response = self.client().patch("/actors/{}.format(r_id)", json=self.edited_actor)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 404)
  #   self.assertFalse(data["success"], True)


  # Start - ISSUE: ERROR, fail to stop input empty value. - 09272228
  # def test_422_update_actor_empty_data(self):
  #   r_id = 1
  #   response = self.client().patch("/actors/{}".format(r_id), json=self.edited_actor_invalid_data)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 422)
  #   self.assertFalse(data["success"], True)
  # End - ISSUE: ERROR, fail to stop input empty value. - 09272228

  # def test_delete_actor(self):
  #   r_id = 12
  #   response = self.client().delete("/actors/{}".format(r_id))
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)
  #   self.assertEqual(data["deleted"], r_id)

  # def test_404_delete_actor_not_exist(self):
  #   r_id = 20549
  #   response = self.client().delete("/actors/{}".format(r_id))
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 404)
  #   self.assertFalse(data["success"], True)
  # --------------------------------------------------
  # Test Actos:GET, POST, PATCH, DELETE - End
  # --------------------------------------------------
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()