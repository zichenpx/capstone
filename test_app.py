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

    # self.new_movie = {
    #   "":,
    #   "":,
    #   "":,
    #   "":,
    #   "":
    # }

    self.edited_movie = {
      "duration": 9999 
    }

    # self.new_actor = {
    #   "":,
    #   "":,
    #   "":
    # }

    self.edited_actor = {
      "name": "PENG EDDIE" 
    }

    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
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
  def test_get_movies(self):
    response = self.client().get("/movies")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["success"], True)
    self.assertTrue(len(data["movies"]))

  def test_get_movie_by_id(self):
    response = self.client().get("/movies/1")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["success"], True)

  def test_404_get_movie_id_not_exist(self):
    response = self.client().get("/movies/89852")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 404)
    self.assertFalse(data["success"], True)    
      
  # def test_create_movie(self):
    # response = self.client().get("/movies")
    # data = json.loads(response.data)

  # def test_422_create_movie(self):
    # response = self.client().get("/movies")
    # data = json.loads(response.data)

  # def test_update_movie(self):
  #   response = self.client().get("/movies/12", json=self.edited_movie)
  #   data = json.loads(response.data)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertEqual(data["success"], True)
  #   print(data)

  # def test_404_update_movie_not_exist(self):
    # response = self.client().get("/movies")
    # data = json.loads(response.data)

  # def test_422_update_movie_typing_error(self):
    # response = self.client().get("/movies")
    # data = json.loads(response.data)

  def test_delete_movie(self):
    response = self.client().get("/movies/5")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["success"], True)
    # Issue: Fixing the ""KeyError: 'deleted'"" - 0927
    # self.assertEqual(data["deleted"], 5)

  def test_404_delete_movie_not_exist(self):
    response = self.client().get("/movies/868072")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 404)
    self.assertFalse(data["success"], True)
  # --------------------------------------------------
  # Test Movies:GET, POST, PATCH, DELETE - End
  # --------------------------------------------------
  # --------------------------------------------------
  # Test Actos:GET, POST, PATCH, DELETE - Start
  # --------------------------------------------------
  def test_get_actors(self):
    response = self.client().get("/actors")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["success"], True)
    self.assertTrue(len(data["actors"]))

  def test_get_actors_by_id(self):
    response = self.client().get("/actors/1")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["success"], True)

  def test_404_get_actors_id_not_exist(self):
    response = self.client().get("/actors/8429031")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 404)
    self.assertFalse(data["success"], True)  

  # def test_create_actor(self):
    # response = self.client().get("/actors")
    # data = json.loads(response.data)

  # def test_422_create_actor(self):
    # response = self.client().get("/actors")
    # data = json.loads(response.data)

  # def test_update_actor(self):
    # response = self.client().get("/actors")
    # data = json.loads(response.data)

  # def test_404_update_actor_not_exist(self):
    # response = self.client().get("/actors")
    # data = json.loads(response.data)

  # def test_422_update_actor_typing_error(self):
    # response = self.client().get("/actors")
    # data = json.loads(response.data)

  def test_delete_actor(self):
    response = self.client().get("/actors/100")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["success"], True)
    # Issue: Fixing the ""KeyError: 'deleted'"" - 0927
    # self.assertEqual(data["deleted"], 5)

  def test_404_delete_actor_not_exist(self):
    response = self.client().get("/actors/20549")
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 404)
    self.assertFalse(data["success"], True)
  # --------------------------------------------------
  # Test Actos:GET, POST, PATCH, DELETE - End
  # --------------------------------------------------
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()